$ ->
  $('a').on
    click: (event) ->
      link = $(this)
      if (link.data('method'))
        event.stopImmediatePropagation()
        event.preventDefault()
        href = link.attr('href')
        method = link.data('method')
        target = link.attr('target')
        csrf_token = $('meta[name=csrf-token]').attr('content')
        csrf_param = $('meta[name=csrf-param]').attr('content')
        form = $('<form method="post" action="' + href + '"></form>')
        metadata_input = '<input name="_method" value="' + method + '" type="hidden" />';

        if (csrf_param != undefined && csrf_token != undefined)
          metadata_input += '<input name="' + csrf_param + '" value="' + csrf_token + '" type="hidden" />'

        if target
          form.attr('target', target)

        form.hide().append(metadata_input).appendTo('body')
        form.submit()

  $('form.search').on
    submit: (event) ->
      event.stopImmediatePropagation()
      event.preventDefault()

      url = $(this).attr('action')
      query = $('[name=query]', this).attr('value')
      
      if not query
        return
      
      query = encodeURIComponent(query)
      
      if query
        location.href = "#{url}/#{query}"

  $('.appear-on-cursol').each ->
    that = $(this)
    appearParent = that.data('appear-parent')
    if appearParent
      that.closest(appearParent).on
        mouseover: ->
          that.removeClass('appear-on-cursol')
        mouseout: ->
          that.addClass('appear-on-cursol')
