"use client";
import { useSession } from "next-auth/react";
import { FaSmileBeam } from "react-icons/fa";

export default function Navbar() {
    const { data: session } = useSession();

    if (!session || !session.user) {
        return <></>;
    }

    return (
        <div className="dui-navbar bg-base-100 fixed top-0 right-0 left-0 z-10">
            <div className="flex-1">
                <a className="dui-btn dui-btn-ghost text-xl">daisyUI</a>
            </div>
            <div className="flex-none gap-2">
                <div className="dui-dropdown dui-dropdown-end">
                    <div
                        tabIndex={0}
                        role="button"
                        className="dui-btn dui-btn-ghost dui-btn-circle dui-avatar overflow-hidden flex items-center justify-center"
                    >
                        <div className="rounded-full flex items-center justify-center">
                            {session.user.image ? (
                                <img
                                    width="30px"
                                    height="30px"
                                    src={session.user.image}
                                />
                            ) : (
                                <FaSmileBeam className="text-[30px]" />
                            )}
                        </div>
                    </div>
                    <ul
                        tabIndex={0}
                        className="dui-menu dui-menu-sm dui-dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
                    >
                        <li>
                            <a className="justify-between">
                                Profile
                                <span className="dui-badge">New</span>
                            </a>
                        </li>
                        <li>
                            <a>Settings</a>
                        </li>
                        <li>
                            <a>Logout</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    );
}
