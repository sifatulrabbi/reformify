import LoginForm from "@/components/LoginForm";

export default function SignInPage() {
    return (
        <main className="w-full flex flex-col justify-center items-center min-h-screen">
            <h2 className="text-2xl mb-8">
                <span className="font-bold opacity-50">Reformify |</span> Login
            </h2>
            <LoginForm />
        </main>
    );
}
