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
