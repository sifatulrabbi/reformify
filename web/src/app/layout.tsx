import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import AuthProvider from "@/providers/AuthProvider";
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

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <AuthProvider>
                <body className={roboto.className}>{children}</body>
            </AuthProvider>
        </html>
    );
}
