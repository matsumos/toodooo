$(function() {
  $('a').on({
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
  $('form.search').on({
    submit: function(event) {
      var query, url;
      event.stopImmediatePropagation();
      event.preventDefault();
      url = $(this).attr('action');
      query = $('[name=query]', this).attr('value');
      if (!query) {
        return;
      }
      query = encodeURIComponent(query);
      if (query) {
        return location.href = "" + url + "/" + query;
      }
    }
  });
  return $('.appear-on-cursol').each(function() {
    var appearParent, that;
    that = $(this);
    appearParent = that.data('appear-parent');
    if (appearParent) {
      return that.closest(appearParent).on({
        mouseover: function() {
          return that.removeClass('appear-on-cursol');
        },
        mouseout: function() {
          return that.addClass('appear-on-cursol');
        }
      });
    }
  });
});
