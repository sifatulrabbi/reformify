import NextAuth, { type AuthOptions } from "next-auth";
import GithubProvider from "next-auth/providers/github";

const secret = process.env.NEXTAUTH_SECRET;
if (!secret) {
    throw new Error("env NEXTAUTH_SECRET not found");
}

export const authOptions: AuthOptions = {
    session: {
        strategy: "jwt",
    },
    pages: {
        signIn: "/auth/login",
    },
    providers: [
        GithubProvider({
            clientId: process.env.GITHUB_CLIENT_ID ?? "",
            clientSecret: process.env.GITHUB_CLIENT_SECRET ?? "",
        }),
    ],
};

export const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
