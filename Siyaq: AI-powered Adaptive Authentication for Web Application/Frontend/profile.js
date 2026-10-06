/* ═══════════════════════════════════════════════════
   profile.js — سياق
   Injects a profile icon into the top-bar when the
   user is logged in (user_id exists in localStorage).
   ═══════════════════════════════════════════════════ */

(function injectProfileIcon() {
    const userId   = localStorage.getItem("user_id");
    const username = localStorage.getItem("username");

    if (!userId) return; // Not logged in — do nothing

    // Wait for DOM to be ready
    function inject() {
        const actions = document.querySelector(".top-actions");
        if (!actions) return;

        // Avoid double-injection
        if (document.getElementById("profileNavBtn")) return;

        // Build the profile button
        const btn = document.createElement("a");
        btn.id   = "profileNavBtn";
        btn.href = "profile.html";
        btn.title = username || "الملف الشخصي";
        btn.style.cssText = `
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(13,110,253,0.15);
            border: 1px solid rgba(13,110,253,0.4);
            color: #fff;
            padding: 6px 14px 6px 10px;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 600;
            text-decoration: none;
            transition: background 0.2s, transform 0.15s;
            cursor: pointer;
            white-space: nowrap;
        `;

        // Avatar circle with initials or icon
        const avatar = document.createElement("span");
        avatar.style.cssText = `
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0d6efd, #00c6ff);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 700;
            color: #fff;
            flex-shrink: 0;
        `;
        const initials = (username || "?")[0].toUpperCase();
        avatar.textContent = initials;

        const label = document.createElement("span");
        label.textContent = username || "الملف الشخصي";
        label.id = "profileNavLabel";

        btn.appendChild(avatar);
        btn.appendChild(label);

        btn.addEventListener("mouseenter", () => {
            btn.style.background = "rgba(13,110,253,0.3)";
            btn.style.transform  = "translateY(-1px)";
        });
        btn.addEventListener("mouseleave", () => {
            btn.style.background = "rgba(13,110,253,0.15)";
            btn.style.transform  = "translateY(0)";
        });

        // Insert before the language buttons
        actions.insertBefore(btn, actions.firstChild);

        // Add a small separator
        const sep = document.createElement("span");
        sep.textContent = "|";
        sep.style.color = "rgba(255,255,255,0.3)";
        sep.style.margin = "0 2px";
        actions.insertBefore(sep, btn.nextSibling);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", inject);
    } else {
        inject();
    }
})();
