//config the reuire.js
console.log('import started!');
requirejs.config({
    baseUrl: '/static/js',
    paths: {
        jquery: 'jquery/jquery-3.4.1',
        // popper: 'https://unpkg.com/@popperjs/core@2/dist/umd/popper',
        // bootstrap: 'bootstrap/bootstrap',
        bootstrap: 'bootstrap/bootstrap.bundle',
        bootstrap_notify: 'bootstrap-notify/bootstrap-notify',
        submit_personal_cabinet_form: 'functions/submit_personal_cabinet_form',
        send_submitted_form: 'functions/send_submitted_form'


    }

    });

console.log('import ended!')
//  <!-- JQuery -->
//         <!-- <script src="/static/js/jquery/jquery-3.4.1.js"></script> -->
//         <!-- Popper -->
//         <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script> -->

//             <!-- Bootstrap JS -->
//             <!-- <script src="/static/js/bootstrap/bootstrap.js"></script> -->

//     <!-- Bootstrap - Notify -->
//         <!-- <script src="/static/js/bootstrap-notify/bootstrap-notify.js"></script>