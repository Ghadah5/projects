/* ═══════════════════════════════════════════════════
   lang.js — سياق | Unified Language & Translation
   Handles: home, about, login, register, forgot-password
   ═══════════════════════════════════════════════════ */

const translations = {
    ar: {
        dir: "rtl",

        /* ── Nav (shared) ── */
        btnAr:            "العربية",
        btnEn:            "English",
        navHome:          "الرئيسية",
        navAbout:         "عن سياق",
        navParticipation: "المشاركة الإلكترونية",
        navServices:      "دليل الخدمات",

        /* ── Home ── */
        bannerBadge: "سياق — خدمة مصادقة رقمية",
        bannerSub:   "سياق تجمع بين الذكاء الاصطناعي والتشفير المتقدم لحماية هويتك الرقمية بأعلى معايير الأمان.",
        ctaLabel:    "ابدأ الآن",
        stat1:       "مستخدم نشط",
        stat2:       "وقت تشغيل مضمون",
        stat3:       "تشفير بت",
        stat4:       "خروقات أمنية",

        /* ── About ── */
        bcHome:           "الرئيسية",
        bcCurrent:        "عن سياق",
        sideMainTitle:    "عن سياق",
        accAboutTitle:    "عن سياق",
        accPoliciesTitle: "السياسات والإجراءات",
        menuAbout:        "عن سياق",
        menuVision:       "الرؤية",
        menuMission:      "الرسالة",
        menuGoals:        "الأهداف",
        menuSystems:      "أنظمة وتعليمات",
        menuTerms:        "شروط الاستخدام",
        aboutTitle:       "عن سياق",
        aboutText1:       "سياق هي خدمة المصادقة الرقمية المتكاملة، وتهدف إلى تقديم خدمات التحقق من الهوية رقمياً للمواطنين والمقيمين والزوار، وذلك من خلال الاستفادة من الإمكانات التقنية، وتسخير التقنيات الحديثة؛ بما يوفر تجربة مستخدم متميزة عبر خدمات مؤتمتة ذات موثوقية وأمان وكفاءة عالية.",
        aboutText2:       "وحققت سياق قفزات كبيرة منذ إطلاقها عبر خدماتها المتقدمة، وأصبحت تنافس منصات المصادقة الرقمية على مستوى العالم، ومن أوائل خدمات التحقق الرقمي على مستوى المنطقة.",
        visionTitle:      "الرؤية",
        visionText:       "تقديم تجربة مصادقة رقمية موثوقة وآمنة تمكّن المستفيدين من الوصول للخدمات بسهولة وفعالية.",
        missionTitle:     "الرسالة",
        missionText:      "تمكين التحول الرقمي لخدمات المصادقة وتطويرها بما يحقق رضا المستفيد ويعزز جودة الحياة.",
        goalsTitle:       "الأهداف",
        goal1:            "رفع كفاءة خدمات المصادقة الإلكترونية وسهولة الوصول.",
        goal2:            "تعزيز أمن المعلومات وحماية بيانات المستخدم.",
        goal3:            "تحسين تجربة المستخدم عبر خدمات مؤتمتة وموثوقة.",
        systemsTitle:     "أنظمة وتعليمات",
        systemsText:      "تُعرض هنا الأنظمة والتعليمات المنظمة لاستخدام سياق والخدمات ذات العلاقة.",
        termsTitle:       "شروط الاستخدام",
        termsText:        "باستخدامك لسياق فأنت توافق على الشروط والأحكام وسياسات الخصوصية والأمان.",

        /* ── Login ── */
        loginTitle:     "تسجيل الدخول",
        loginUserLabel: "اسم المستخدم",
        loginPassLabel: "كلمة المرور",
        forgotPass:     "نسيت كلمة المرور؟",
        loginBtn:       "تسجيل الدخول",
        newUserText:    "مستخدم جديد؟",
        createAccount:  "إنشاء حساب",

        /* ── Forgot Password ── */
        forgotTitle:      "استعادة كلمة المرور",
        forgotText:       "أدخل بريدك الإلكتروني المسجّل في سياق، وسنرسل لك رابط إعادة تعيين كلمة المرور",
        forgotEmailLabel: "البريد الإلكتروني",
        forgotBtn:        "إرسال رابط الاستعادة",
        backToLogin:      "← العودة لتسجيل الدخول",

        /* ── Register ── */
        registerTitle:  "تسجيل مستخدم جديد",
        idLabel:        "رقم الهوية أو الإقامة أو الحدود",
        firstNameLabel: "الاسم الأول",
        lastNameLabel:  "اسم العائلة",
        mobileLabel:    "رقم الجوال",
        emailLabel:     "عنوان البريد الإلكتروني",
        usernameLabel:  "اسم المستخدم",
        passwordLabel:  "كلمة المرور",
        confirmLabel:   "تأكيد كلمة المرور",
        registerBtn:    "تسجيل",
        backLogin:      "العودة لتسجيل الدخول",
       
       /* ── Reset Password ── */
        resetTitle:      "إعادة تعيين كلمة المرور",
        resetText:       "أدخل كلمة المرور الجديدة وسيتم تحديثها لحسابك",
        newPassword:     "كلمة المرور الجديدة",
        confirmPassword: "تأكيد كلمة المرور",
        passwordRules:   "يجب أن تحتوي كلمة المرور على: 8 أحرف على الأقل، حرف كبير، حرف صغير، ورقم",
        resetBtn:        "إعادة التعيين",

        /* ── MFA / OTP ── */
        mfaTitle:       "التحقق بخطوتين",
        mfaSubtext:     "أُرسل رمز التحقق إلى بريدك الإلكتروني",
        verifyBtn:      "تحقق من الرمز",
        timerLabel:     "انتهاء الرمز خلال",
        resendBtn:      "إعادة الإرسال",
        mfaBackToLogin: "← العودة لتسجيل الدخول",
    },


    en: {
        dir: "ltr",

        /* ── Nav (shared) ── */
        btnAr:            "Arabic",
        btnEn:            "English",
        navHome:          "Home",
        navAbout:         "About Siyaq",
        navParticipation: "E-Participation",
        navServices:      "Services Guide",

        /* ── Home ── */
        bannerBadge: "Siyaq — Digital Authentication Service",
        bannerSub:   "Siyaq combines AI and advanced encryption to protect your digital identity with the highest security standards.",
        ctaLabel:    "Get Started",
        stat1:       "Active Users",
        stat2:       "Guaranteed Uptime",
        stat3:       "Bit Encryption",
        stat4:       "Security Breaches",

        /* ── About ── */
        bcHome:           "Home",
        bcCurrent:        "About Siyaq",
        sideMainTitle:    "About Siyaq",
        accAboutTitle:    "About Siyaq",
        accPoliciesTitle: "Policies & Procedures",
        menuAbout:        "About Siyaq",
        menuVision:       "Vision",
        menuMission:      "Mission",
        menuGoals:        "Goals",
        menuSystems:      "Systems & Instructions",
        menuTerms:        "Terms of Use",
        aboutTitle:       "About Siyaq",
        aboutText1:       "Siyaq is an integrated digital authentication service aimed at providing identity verification digitally for citizens, residents, and visitors, leveraging technical capabilities and modern technologies to deliver a superior user experience through automated, reliable, secure, and efficient services.",
        aboutText2:       "Siyaq has achieved significant milestones since its launch through its advanced services, and has become competitive with digital authentication platforms globally, and among the first digital verification services in the region.",
        visionTitle:      "Vision",
        visionText:       "Deliver a trusted and secure digital authentication experience that enables users to access services with ease and efficiency.",
        missionTitle:     "Mission",
        missionText:      "Enable digital transformation of authentication services and develop them to achieve user satisfaction and enhance quality of life.",
        goalsTitle:       "Goals",
        goal1:            "Enhance the efficiency of electronic authentication services and ease of access.",
        goal2:            "Strengthen information security and protect user data.",
        goal3:            "Improve user experience through automated and reliable services.",
        systemsTitle:     "Systems & Instructions",
        systemsText:      "The systems and instructions governing the use of Siyaq and related services are presented here.",
        termsTitle:       "Terms of Use",
        termsText:        "By using Siyaq you agree to the terms, conditions, privacy and security policies.",

        /* ── Login ── */
        loginTitle:     "Sign In",
        loginUserLabel: "Username",
        loginPassLabel: "Password",
        forgotPass:     "Forgot your password?",
        loginBtn:       "Sign In",
        newUserText:    "New user?",
        createAccount:  "Create Account",

        /* ── Forgot Password ── */
        forgotTitle:      "Password Recovery",
        forgotText:       "Enter your registered Siyaq email address and we will send you a password reset link.",
        forgotEmailLabel: "Email Address",
        forgotBtn:        "Send Recovery Link",
        backToLogin:      "← Back to Sign In",

        /* ── Register ── */
        registerTitle:  "New User Registration",
        idLabel:        "National ID / Residence / Border Number",
        firstNameLabel: "First Name",
        lastNameLabel:  "Last Name",
        mobileLabel:    "Mobile Number",
        emailLabel:     "Email Address",
        usernameLabel:  "Username",
        passwordLabel:  "Password",
        confirmLabel:   "Confirm Password",
        registerBtn:    "Register",
        backLogin:      "Back to Sign In",
       
        /* ── Reset Password ── */
        resetTitle:      "Reset Password",
        resetText:       "Enter your new password to update your account",
        newPassword:     "New Password",
        confirmPassword: "Confirm Password",
        passwordRules:   "Password must include: at least 8 characters, uppercase, lowercase, and number",
        resetBtn:        "Reset",
        
        /* ── MFA / OTP ── */
        mfaTitle:       "Two-Step Verification",
        mfaSubtext:     "A verification code has been sent to your email",
        verifyBtn:      "Verify Code",
        timerLabel:     "Code expires in",
        resendBtn:      "Resend Code",
        mfaBackToLogin: "← Back to Sign In",
    }
};

/* ── Typing animation (home page only) ── */
const typingPhrases = {
    ar: ["مصادقة أذكى", "أمان أعلى", "هوية موثوقة", "حماية لا تُهزم"],
    en: ["Smarter Authentication", "Superior Security", "Trusted Identity", "Unbreakable Protection"]
};

let _currentLang = 'ar';
let _phraseIndex  = 0;
let _charIndex    = 0;
let _isDeleting   = false;
let _typingTimer;

function _typeEffect() {
    const el = document.getElementById('typingText');
    if (!el) return; // not on home page

    const list   = typingPhrases[_currentLang];
    const phrase = list[_phraseIndex % list.length];

    if (!_isDeleting) {
        el.textContent = phrase.slice(0, _charIndex + 1);
        _charIndex++;
        if (_charIndex === phrase.length) {
            _isDeleting = true;
            _typingTimer = setTimeout(_typeEffect, 1800);
            return;
        }
    } else {
        el.textContent = phrase.slice(0, _charIndex - 1);
        _charIndex--;
        if (_charIndex === 0) { _isDeleting = false; _phraseIndex++; }
    }

    _typingTimer = setTimeout(_typeEffect, _isDeleting ? 55 : 90);
}

/* ── Main setLang function ── */
function setLang(lang) {
    _currentLang = lang;
    const t = translations[lang];

    document.documentElement.lang = lang;
    document.documentElement.dir  = t.dir;

    for (const key in t) {
        if (key === 'dir') continue;
        const el = document.getElementById(key);
        if (el) el.innerText = t[key];
    }

    // Reset typing if on home page
    const typingEl = document.getElementById('typingText');
    if (typingEl) {
        clearTimeout(_typingTimer);
        _phraseIndex = 0; _charIndex = 0; _isDeleting = false;
        typingEl.textContent = '';
        _typeEffect();
    }
}

// Init on page load
setLang(document.documentElement.lang || 'ar');
