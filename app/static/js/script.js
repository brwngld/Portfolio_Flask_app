document.addEventListener("DOMContentLoaded", function() {
    var firstInput = document.getElementById("firstNumberInput");
    if (firstInput) firstInput.focus();

    var calculatorForm = document.getElementById("calculatorForm");
    if (calculatorForm) {
        calculatorForm.addEventListener("submit", function() {
            const first_number = document.getElementById("firstNumberInput").value;
            const second_number = document.getElementById("secondNumberInput").value;
            const operation = document.getElementById("operationSelect").value;

            fetch("/calculator/api/calculate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    first_number: first_number,
                    second_number: second_number,
                    operation: operation
                })
            })
            .then(response => response.json())
            .then(data => {
                let resultArea = document.getElementById("resultArea");
                if (data.error) {
                    resultArea.innerHTML = `<div class="alert alert-danger mt-4"><h4 class="mb-0">${data.error}</h4></div>`;
                } else {
                    resultArea.innerHTML = `<div class="alert alert-info mt-4"><h4 class="mb-0">Result: ${data.result}</h4></div>`;
                }
            });
        });
    }
});

setTimeout(function() {
  var alerts = document.querySelectorAll('.alert');
  alerts.forEach(function(alert) {
    var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
    bsAlert.close();
  });
}, 4000);
// Auto-dismiss alerts after 4 seconds
  window.setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
      bootstrap.Alert.getOrCreateInstance(alert).close();
    });
  }, 4000);
