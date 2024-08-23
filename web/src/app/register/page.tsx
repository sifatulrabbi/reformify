import Link from "next/link";
import RegistrationForm from "@/components/RegistrationForm";

export default async function RegistrationPage() {
    return (
        <main className="w-full flex flex-col justify-center items-center min-h-screen">
            <h2 className="text-2xl mb-8">
                <span className="font-bold opacity-50">Reformify |</span>{" "}
                Register
            </h2>
            <RegistrationForm />
            <div className="text-md">
                Already have an account?{" "}
                <Link href="/" className="dui-link dui-link-primary">
                    Login
                </Link>
            </div>
        </main>
    );
}
