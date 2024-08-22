import NextAuth, { type AuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

const secret = process.env.NEXTAUTH_SECRET;
if (!secret) {
    throw new Error("env NEXTAUTH_SECRET not found");
}

export const authOptions: AuthOptions = {
    secret,

    session: {
        strategy: "jwt",
    },

    pages: {
        signIn: "/",
        signOut: "/",
        error: "/auth/error",
    },

    providers: [
        CredentialsProvider({
            name: "Credentials",
            credentials: {
                email: { label: "Email", type: "email" },
                password: { label: "Password", type: "password" },
            },
            authorize: async (credentials, req) => {
                console.log("\n\nauthorize()\n\n");
                try {
                    const res = await fetch(
                        `${process.env.NEXT_PUBLIC_API_URL}/auth/login`,
                        {
                            method: "POST",
                            body: JSON.stringify(credentials || {}),
                            headers: { "Content-Type": "application/json" },
                        },
                    );
                    const data = await res.json();
                    if (res.ok && data.user && data.user.email) {
                        return data.user;
                    }
                    return null;
                } catch (err) {
                    console.error(err);
                    return null;
                }
            },
        }),
    ],

    // callbacks: {
    //     jwt: async ({ token, user, account }) => {
    //         console.log("from jwt:", token, user, account);
    //         if (user && user.access_token) {
    //             token.accessToken = user.access_token;
    //         } else if (account && account.access_token) {
    //             token.accessToken = account.access_token;
    //         }
    //         return token;
    //     },
    //
    //     session: async ({ session, token, user }) => {
    //         console.log("from session:", session, token, user);
    //         session.access_token = token.access_token;
    //         return session;
    //     },
    //
    //     async signIn({ user, account, profile, email, credentials }) {
    //         console.log(
    //             "from signIn:",
    //             user,
    //             account,
    //             profile,
    //             email,
    //             credentials,
    //         );
    //         return false;
    //     },
    //
    //     async redirect({ url, baseUrl }) {
    //         console.log("from redirect:", url, baseUrl);
    //         return baseUrl;
    //     },
    // },
};

export default NextAuth(authOptions);
