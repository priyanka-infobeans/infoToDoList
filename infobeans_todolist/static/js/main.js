$(document).ready(function() {
    $('.delete-link').on('click', function(event) {alert('hi');
      event.preventDefault();
      var blogId = $(this).data('blog-id');
      var confirmDelete = confirm('Are you sure you want to delete this blog?');
      if (confirmDelete) {
        $.ajax({
          url: '{% url 'blog_app:blog_delete' pk=0 %}'.replace('0', blogId),
          method: 'POST',
          success: function() {
            window.location.reload();
          },
          error: function() {
            alert('An error occurred while deleting the blog.');
          }
        });
      }
    });
  if ($('.task-checkbox').is(':checked')) {
    $(this).next('#task-title').css('text-decoration', 'line-through');
  } else {
    $(this).next('#task-title').css('text-decoration', '');
  }

  $('.task-checkbox').change(function() {
    var taskId = $(this).data('task-id');
    var isChecked = $(this).is(':checked');

    if ($(this).is(':checked')) {
      $(this).next('#task-title').addClass('task-title-line-through');
    } else {
      $(this).next('#task-title').removeClass('task-title-line-through');
    }
    // Send an AJAX request to update the title_status in the database
    var csrftoken =  $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
          url: '/todolist_app/update_title_status/',  // Replace with the appropriate URL
          type: 'POST',
          data: {
            task_id: taskId,
            is_checked: isChecked,
            csrfmiddlewaretoken: csrftoken
          },
          success: function(response) {alert('step2');
            console.log('Title status updated successfully.');
          },
          error: function(xhr, textStatus, error) {
            console.log('Error updating title status:', error);
          }
        });
    });
});