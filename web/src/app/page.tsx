import Link from "next/link";
import LoginForm from "@/components/LoginForm";

export default function HomePage() {
    return (
        <main className="w-full flex flex-col justify-center items-center min-h-screen">
            <h2 className="text-4xl font-bold mb-8">Reformify</h2>
            <LoginForm />
            <div className="text-md">
                Don&apos;t have an account?{" "}
                <Link href="/register" className="dui-link dui-link-primary">
                    Register
                </Link>
            </div>
        </main>
    );
}
