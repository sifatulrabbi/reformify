import Link from "next/link";
import { FaGithub } from "react-icons/fa";

export default function HomePage() {
    return (
        <main className="w-full flex flex-col justify-center items-center min-h-screen p-6">
            <h2 className="text-4xl font-bold mb-8">Reformify</h2>

            <div className="w-full max-w-[300px] flex flex-col items-center gap-6">
                <Link
                    href="/auth/login"
                    className="dui-btn dui-btn-primary w-full"
                >
                    Login with Password
                </Link>
                <Link href="/api/auth/signin" className="dui-btn w-full">
                    <FaGithub />
                    Continue with GitHub
                </Link>
            </div>
        </main>
    );
}
