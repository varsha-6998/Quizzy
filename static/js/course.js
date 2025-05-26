function enrollCourse(courseName, event) {
    if (!isLoggedIn) {
        if (confirm("🚫 You need to log in to enroll. Go to Sign In page?")) {
            window.location.href = "/signin";
        }
        return;
    }

    alert(`You're being redirected to registration for ${courseName}.`);

    // button animation (optional)
    event.target.style.background = 'linear-gradient(135deg, #10b981, #059669)';
    event.target.innerHTML = '✓ Enrolled!';

    // redirect after short delay so user can see animation
    setTimeout(() => {
        window.location.href = "/registration?course=" + encodeURIComponent(courseName);
    }, 1500);
}
