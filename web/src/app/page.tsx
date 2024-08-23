import LoginForm from "@/components/LoginForm";

export default function HomePage() {
    return (
        <main className="w-full flex flex-col justify-center items-center min-h-screen">
            <h2 className="text-4xl font-bold mb-8">Reformify</h2>
            <LoginForm />
        </main>
    );
}
