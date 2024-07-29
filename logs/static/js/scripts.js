$(document).ready(function() {
    if (localStorage.getItem('dark-mode') === 'enabled') {
        $('body').addClass('dark-mode');
    }

    $('#toggle-theme').click(function() {
        $('body').toggleClass('dark-mode');
        if ($('body').hasClass('dark-mode')) {
            localStorage.setItem('dark-mode', 'enabled');
        } else {
            localStorage.setItem('dark-mode', 'disabled');
        }
    });

    $('#filter-form').submit(function(event) {
        event.preventDefault();
        updateLogs($(this));
    });

    $(document).on('click', '.pagination .page-link', function(event) {
        event.preventDefault();
        var url = $(this).attr('href');
        updateLogsFromUrl(url);
    });

    function updateLogs(form) {
        var url = '/logs/?' + form.serialize();
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('#logs-container').html(data.html);
                highlightNumbers();
            },
            error: function(xhr) {
                console.error("AJAX request failed: ", xhr.responseText);
            }
        });
    }

    function updateLogsFromUrl(url) {
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('#logs-container').html(data.html);
                highlightNumbers();
            },
            error: function(xhr) {
                console.error("AJAX request failed: ", xhr.responseText);
            }
        });
    }

    function highlightNumbers() {
        $('.log-message').each(function() {
            var html = $(this).html();
            html = html.replace(/(\d+)/g, '<span class="number">$1</span>');
            $(this).html(html);
        });
    }

    highlightNumbers();
});
