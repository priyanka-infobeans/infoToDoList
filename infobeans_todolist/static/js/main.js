$(document).ready(function() {
  if ($('.task-checkbox').is(':checked')) {
    $(this).next('#task-title').css('text-decoration', 'line-through');
  } else {
    $(this).next('#task-title').css('text-decoration', '');
  }

  $('.task-checkbox').change(function() {
    if ($(this).is(':checked')) {
      $(this).next('#task-title').addClass('task-title-line-through');
    } else {
      $(this).next('#task-title').removeClass('task-title-line-through');
    }
  });
})