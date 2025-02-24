function updateGoldDisplay() {
    $.ajax({
        url: '/get_gold/',  // ✅ Calls Django API
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            if (data.gold !== undefined) {
                $("#gold-display").text(`${data.gold}🟡`);  // ✅ Update UI
            }
        },
        error: function(xhr, status, error) {
            console.error("❌ Failed to update gold:", error);
        }
    });
}

// Auto-refresh gold every 5 seconds
setInterval(updateGoldDisplay, 5000);
