document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    dateClick: function(info) {
      document.getElementById('deadline').value = info.dateStr;
      add_task_modal.showModal()
    },

    eventClick: function(info) {

      // edit_task_modal.showModal()

      var title = info.event.title;
      var start = info.event.start ;
      var description = info.event.extendedProps.description || '';
      var id = info.event.id;

      edit_task_modal.showModal()


    },  

    initialView: 'dayGridMonth',
    initialDate: new Date(),
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    events: window.calendarEvents // <-- Use your JSON here
  });

  calendar.render();
});


