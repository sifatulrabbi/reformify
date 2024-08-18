"use client";
import { useSession, signIn } from "next-auth/react";

export default function ProfilePage() {
  const { data: session } = useSession();

  return (
    <main className="w-full flex flex-col justify-start items-start p-6">
      <div className="w-full flex items-center pb-6 text-sm font-bold text-primary">
        Your Profile
      </div>
      {session && (
        <div className="w-full flex flex-col gap-6">
          You're logged in!
          <div className="w-full flex flex-row items-center justify-start"></div>
        </div>
      )}
      {!session && (
        <>
          <div className="w-full flex flex-col gap-6 mb-6">
            You're not logged in!
          </div>
          <button onClick={() => signIn()} className="dui-btn dui-btn-primary">
            Sign In
          </button>
        </>
      )}
    </main>
  );
}
