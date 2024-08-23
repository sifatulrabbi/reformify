import { useSession } from "next-auth/react";

export default function ProfilePage() {
    return (
        <main className="w-full flex flex-col justify-start items-start p-6">
            <div className="w-full flex items-center pb-6 text-sm font-bold text-primary">
                Your Profile
            </div>
            <div className="w-full flex flex-col gap-6">
                You're logged in!
                <div className="w-full flex flex-row items-center justify-start"></div>
            </div>
        </main>
    );
}
