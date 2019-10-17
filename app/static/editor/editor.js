jQuery(function($) {
  var script_json = $("#script").val(); 

  window.form_get_query = function() {
    setListData();
    //console.log(listData);
    $('#result').html("");
    $.each(listData, function(i, d) {
      $('#result').append("<p>("+d.type+") => ("+d.source+")</p>");
    });
  }

  function get_query() {
    setListData();
    console.log(listData);
    $('#result').html("");
    $.each(listData, function(i, d) {
      $('#result').append("<p>("+d.type+") => ("+d.source+")</p>");
    });
  }
  var bno = 1;

  function add_input_box(type, source) {
	 inputboxli = '<li class="input-box" id="ibid_'+bno+'">' +
		  '<ul class="input-box-heading item-head-tools list-unstyled">' +
		  '<li id="mover-tool" class="item-tool"><span class="glyphicon glyphicon-move"></span></li>' +
		  '<li id="type-tool" class="item-tool" data-type="script">' +
		  '<div class="dropdown">' +
		  '<div class="dropdown-toggle" type="button" data-toggle="dropdown"><span class="item-type">' + type + '</span>' +
		  '<span class="caret"></span>' +
		  '</div>' +
		  '<ul class="dropdown-menu">' +
		  '<li><a href="#" data-value="script" class="type-select">Script</a></li>' +
		  '<li><a href="#" data-value="html" class="type-select">HTML</a></li>' +
		  '<li><a href="#" data-value="h1" class="type-select">Heading 1</a></li>' +
		  '</ul>' +
		  '</div>' +
		  '</li>' +
		  '<li id="type-tool" class="item-tool">' +
		  '<div class="dropdown">' +
		  '<div class="dropdown-toggle" type="button" data-toggle="dropdown"><span class="glyphicon glyphicon-option-vertical"></span>' +
		  '</div>' +
		  '<ul class="dropdown-menu">' +
		  '<li><a href="#deletblock" class="delete-block-item">Delete this block</a></li>' +
		  '</ul>' +
		  '</div>' +
		  '</li>' +
		  '</ul>' +
		  '<div class="input-box-editor">' +
		  '<textarea class="text-editor" rows=1>' + source + '</textarea>' +
		  '</div>' +
		  '<div id="ibid_pre_'+bno+'" class="output-preview"></div>' +			
		  '</li>';

    $('#draggablePanelList').append(inputboxli);

	/*
	$('.delete-block-item').click(function() {
		$(this).closest("li.input-box").remove();
	});

    $('.text-editor').keydown(function (e) {
		if (e.keyCode == 9){
            var val = this.value,
			start = this.selectionStart,
			end = this.selectionEnd;

            // set textarea value to: text before caret + tab + text after caret
            this.value = val.substring(0, start) + '\t' + val.substring(end);

            // put caret at right position again
            this.selectionStart = this.selectionEnd = start + 1;

            // prevent the focus lose
            return false;
		}

		if (e.ctrlKey == 13) {

		}

		if (e.ctrlKey && e.keyCode == 13) {

		}

		if (e.keyCode == 13) {
			if(e.shiftKey){
				alert("Query!!");
				e.preventDefault();
			} else {

			}
		}
    });

    $(".type-select").click(function() {
      selected = $(this).attr("data-value");
      $(this).closest("li.item-tool").find(".item-type").html(selected);
      //alert($(this).attr("data-value"));
    });
	*/

	add_input_box_event(bno);
	bno++;
  }

  function add_input_box_event(bid)
  {
	input_box = $('#ibid_'+bid);

    input_box.find('.text-editor').keydown(function (e) {
		if (e.keyCode == 9){
            var val = this.value,
			start = this.selectionStart,
			end = this.selectionEnd;

            // set textarea value to: text before caret + tab + text after caret
            this.value = val.substring(0, start) + '\t' + val.substring(end);

            // put caret at right position again
            this.selectionStart = this.selectionEnd = start + 1;

            // prevent the focus lose
            return false;
		}

		if (e.ctrlKey == 13) {

		}

		if (e.ctrlKey && e.keyCode == 13) {

		}

		if (e.keyCode == 13) {
			if(e.shiftKey){
				run_response(bid, $(this).val());
				e.preventDefault();
			} else {

			}
		}
    });

    input_box.find(".type-select").click(function() {
      selected = $(this).attr("data-value");
      $(this).closest("li.item-tool").find(".item-type").html(selected);
      //alert($(this).attr("data-value"));
    });

	input_box.find('.delete-block-item').click(function() {
		$(this).closest("li.input-box").remove();
	});

  }

  try
  {
	var script = $.parseJSON(script_json);
	$.each(script, function(i,d) {
	  add_input_box(d.type, d.source);
	});
  }
  catch (err)
  {
	add_input_box("script", "");
  }

  autosize(document.querySelectorAll('textarea'));

  $(".add-console-btn").click(function() {
    add_input_box("script","");
    autosize(document.querySelectorAll('textarea'));
  });

  $('#query_btn').click(function() {
    setListData();
    console.log(listData);
    $('#result').html("");
    $.each(listData, function(i, d) {
      $('#result').append("<p>("+d.type+") => ("+d.source+")</p>");
    });
  });

  var listData = [];
  setListData = function() {
    listData = [];
    panelList.find(".input-box").each(function(index) {
      editor = $(this).find(".text-editor");
      type = $(this).find(".item-type");
      listData.push({
        "type": type.text(),
        "source": editor.val()
      });
	  $('#json_value').html(JSON.stringify(listData));
    });
  }

  function getTime()
  {
    return new Date().getTime();
  }

  addItemMore = function(selector) {
    itemid = getTime();
    var itemadd = "<div class='jc-item'>" +
        "<div class='row'>" +
        "</div>" +
        "</div>";

    selector.append(itemadd).find('.jc-item-check').blur(function() {
      addBlurEvent($(this));				
    });

  }

  var $sectionListItem;
  var $itemListItem;

  var panelList = $('#draggablePanelList');

  try {
    panelList.sortable({
      // Only make the .panel-heading child elements support dragging.
      // Omit this to make then entire <li>...</li> draggable.
      handle: '.input-box-heading', 
      update: function() {
        $('.input-box', panelList).each(function(index, elem) {
          var $sectionListItem = $(elem),
              newIndex = $sectionListItem.index();

          // Persist the new indices.
        });
        //setListData();
        //console.log(setListData());
      }
    });
  } catch(err) {
    console.log(err);
  }
  //autosize('.text-editor');
});