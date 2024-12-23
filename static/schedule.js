// Delete Schedule Functionality
$(document).off('click', '.delete-schedule').on('click', '.delete-schedule', function (event) {
    event.preventDefault();
    var scheduleId = $(this).data('id');
    console.log(`Delete button clicked for Schedule ID: ${scheduleId}`);

    // Confirm deletion
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    // Add a spinner to the button for visual feedback
    var $button = $(this);
    $button.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');

    // Perform AJAX request
    $.ajax({
        type: 'POST',
        url: '/delete_schedule/' + scheduleId,
        success: function () {
            console.log(`Task with Schedule ID ${scheduleId} successfully deleted.`);
            
            // Highlight the row before removing it
            var $row = $button.closest('tr');
            $row.css('background-color', '#ffcccc');
            setTimeout(() => $row.remove(), 500); // Delay to show the highlight
        },
        error: function (xhr, status, error) {
            console.error(`Error deleting schedule with ID ${scheduleId}:`, xhr.responseText);
            alert('Error deleting schedule. Please try again.');
        },
        complete: function () {
            // Re-enable the button and restore its original text
            $button.prop('disabled', false).html('Delete');
        }
    });
});

// Task Status Update Functionality
$(document).ready(function () {
    // When the checkbox is clicked, update the task status and appearance
    $('.task-checkbox').on('change', function () {
        var taskRow = $(this).closest('tr');
        var taskId = $(this).data('id');
        var isChecked = $(this).prop('checked');
        
        // Perform AJAX request to update the status in the database
        $.ajax({
            type: 'POST',
            url: '/update_task_status/' + taskId,
            data: { status: isChecked ? 'done' : 'to-do' },
            success: function () {
                // Update the UI based on checkbox state
                if (isChecked) {
                    taskRow.find('.task-name').css('text-decoration', 'line-through');
                    taskRow.find('.task-status').text('Done');
                    taskRow.find('.edit-button').addClass('disabled').prop('disabled', true);
                } else {
                    taskRow.find('.task-name').css('text-decoration', 'none');
                    taskRow.find('.task-status').text('To-Do');
                    taskRow.find('.edit-button').removeClass('disabled').prop('disabled', false);
                }
            },
            error: function () {
                alert('Error updating task status. Please try again.');
            }
        });
    });

    // Task Filtering Functionality
    $('#status-filter').on('change', function () {
        var filterValue = $(this).val();
        $('.schedule-item').each(function () {
            var taskStatus = $(this).data('status');
            if (filterValue === 'all' || taskStatus === filterValue) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("themeToggle");
    const body = document.body;

    // Load theme preference from localStorage
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        body.setAttribute("data-theme", savedTheme);
        themeToggle.textContent = savedTheme === "dark" ? "☀️" : "🌙";
    }

    // Toggle theme on button click
    themeToggle.addEventListener("click", () => {
        const currentTheme = body.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        body.setAttribute("data-theme", newTheme);
        themeToggle.textContent = newTheme === "dark" ? "☀️" : "🌙";
        localStorage.setItem("theme", newTheme);
    });
});
const themeToggleButton = document.getElementById('themeToggle');

themeToggleButton.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
});
