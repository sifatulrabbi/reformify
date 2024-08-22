import { useRouter } from "next/router";

export default function AuthErrorPage() {
    const router = useRouter();
    console.log(router);

    return (
        <div className="w-full flex flex-col">
            <h1 className="text-xl">Something went wrong please try again!</h1>
        </div>
    );
}
