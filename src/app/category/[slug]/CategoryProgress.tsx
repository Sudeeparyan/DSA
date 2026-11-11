"use client";

import { useEffect, useState } from "react";
import { countByStatus } from "@/lib/progress";

export function CategoryProgress({ slugs }: { slugs: string[] }) {
  const [text, setText] = useState(`${slugs.length} problems`);
  useEffect(() => {
    const c = countByStatus(slugs);
    setText(
      `${c.understood} understood · ${c.learning} learning · ${c.need_revision} revise · ${c.not_started} not started`,
    );
  }, [slugs]);
  return <p className="text-sm text-muted">{text}</p>;
}
