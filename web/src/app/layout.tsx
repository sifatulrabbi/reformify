import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import AuthProvider from "@/providers/AuthProvider";
import Navbar from "@/components/Navbar";
import { getServerSession } from "next-auth";
import "./globals.css";

const roboto = Roboto({
    subsets: ["latin"],
    weight: ["100", "300", "400", "500", "700", "900"],
    style: ["normal", "italic"],
});

export const metadata: Metadata = {
    title: "Reformify - Easier job search",
    description: "Reformify - Easier job search",
};

export default async function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    const session = await getServerSession();

    return (
        <html lang="en" data-theme="dark">
            <body className={`${roboto.className} pt-[64px]`}>
                <AuthProvider session={session}>
                    <Navbar />
                    {children}
                </AuthProvider>
            </body>
        </html>
    );
}
