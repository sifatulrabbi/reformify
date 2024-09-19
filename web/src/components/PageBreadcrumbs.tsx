"use client";

import { useSession } from "next-auth/react";
import { usePathname } from "next/navigation";
import Link from "next/link";
import { Fragment, useEffect, useState } from "react";
import { startCase } from "lodash";

type PathEntry = {
    title: string;
    href: string;
};

export default function PageBreadcrumbs() {
    const [pathEntries, setPathEntries] = useState<PathEntry[]>([]);
    const { data: session } = useSession();
    const pathname = usePathname();

    useEffect(() => {
        const entries: PathEntry[] = [];
        const names: PathEntry[] = [];
        for (const p of pathname.split("/")) {
            if (!p) continue;
            const entry = {
                title: startCase(p),
                href: names.join("/") + "/" + p,
            };
            entries.push(entry);
        }
        setPathEntries(entries);
    }, [pathname, session]);

    if (!session || !session.user) {
        return <></>;
    }

    return (
        <div className="w-full flex items-center justify-start gap-1 px-6 py-4 text-sm">
            <Link href="/dashboard">Dashboard</Link>
            {pathEntries.map((p) => (
                <Fragment key={p.href}>
                    <span>/</span>
                    <Link href={pathname} className="text-sm">
                        {p.title}
                    </Link>
                </Fragment>
            ))}
        </div>
    );
}
