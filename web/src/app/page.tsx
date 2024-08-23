import Link from "next/link";
import { FaGithub } from "react-icons/fa";

export default function HomePage() {
    return (
        <main className="w-full flex flex-col justify-center items-center min-h-screen">
            <h2 className="text-4xl font-bold mb-8">Reformify</h2>

            <div className="w-full max-w-[90%] lg:max-w-xl flex flex-col items-center gap-6">
                <Link href="/auth/login" className="dui-btn dui-btn-primary">
                    Login with Password
                </Link>
                <Link href="/auth/login" className="dui-btn">
                    <FaGithub />
                    Continue with GitHub
                </Link>
            </div>
        </main>
    );
}
