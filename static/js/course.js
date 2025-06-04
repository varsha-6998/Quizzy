function enrollCourse(courseId, event) {
    if (isLoggedIn !== "true") {
        if (confirm("🚫 You need to log in to enroll. Go to Sign In page?")) {
            window.location.href = "/signin";
        }
        return;
    }

    // Update button UI
    event.target.disabled = true;
    event.target.innerHTML = "⏳ Enrolling...";
    event.target.style.background = "#06b6d4";

    // Make POST request to enroll
    fetch("/enroll", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ course_id: courseId })  
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            event.target.innerHTML = "✓ Enrolled!";
            event.target.style.background = "linear-gradient(135deg, #10b981, #059669)";
        } else {
            alert("❌ Enrollment failed: " + data.message);
            event.target.innerHTML = "Enroll Now";
            event.target.disabled = false;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong.");
        event.target.innerHTML = "Enroll Now";
        event.target.disabled = false;
    });
}
