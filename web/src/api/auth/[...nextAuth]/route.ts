import NextAuth, { type AuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions: AuthOptions = {
  secret: process.env.NEXTAUTH_SECRET,

  session: {
    strategy: "jwt",
  },

  pages: {
    signIn: "/",
    signOut: "/",
  },

  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },

      authorize: async (credentials, req) => {
        try {
          const res = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}/auth/login`,
            {
              method: "POST",
              body: JSON.stringify({
                email: credentials?.email,
                password: credentials?.password,
              }),
              headers: { "Content-Type": "application/json" },
            },
          );
          const data = await res.json();
          if (data.user && data.user.email) {
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

  callbacks: {
    jwt: async ({ token, user }) => {
      if (user) {
        token.user = user;
        token.accessToken = user.token;
      }
      // Decode the JWT to access its payload
      if (token.accessToken) {
        const decoded = jwt.decode(token.accessToken);
        const now = Math.floor(Date.now() / 1000);
        if (
          decoded &&
          typeof decoded === "object" &&
          "exp" in decoded &&
          decoded.exp &&
          decoded.exp < now
        ) {
          // Invalidate the token by deleting the accessToken
          delete token.accessToken;
        }
      }
      return token;
    },

    session: async ({ session, token, user }) => {
      console.log(session, token, user);
      return session;
    },
  },
};

export default NextAuth(authOptions);
