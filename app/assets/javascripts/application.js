$(function() {
  return $('a').on({
    click: function(event) {
      var csrf_param, csrf_token, form, href, link, metadata_input, method, target;
      link = $(this);
      if (link.data('method')) {
        event.stopImmediatePropagation();
        event.preventDefault();
        href = link.attr('href');
        method = link.data('method');
        target = link.attr('target');
        csrf_token = $('meta[name=csrf-token]').attr('content');
        csrf_param = $('meta[name=csrf-param]').attr('content');
        form = $('<form method="post" action="' + href + '"></form>');
        metadata_input = '<input name="_method" value="' + method + '" type="hidden" />';
        if (csrf_param !== void 0 && csrf_token !== void 0) {
          metadata_input += '<input name="' + csrf_param + '" value="' + csrf_token + '" type="hidden" />';
        }
        if (target) {
          form.attr('target', target);
        }
        form.hide().append(metadata_input).appendTo('body');
        return form.submit();
      }
    }
  });
});
