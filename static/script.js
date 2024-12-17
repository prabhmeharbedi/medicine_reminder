document.getElementById("reminderForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const data = {
        email: document.getElementById("email").value,
        medicine_name: document.getElementById("medicine_name").value,
        dosage: document.getElementById("dosage").value,
        reminder_time: document.getElementById("reminder_time").value
    };

    fetch("/add_reminder", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => alert(data.message));
});