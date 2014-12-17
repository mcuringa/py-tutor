//foo

//make underscore templates look like django templates
_.templateSettings = {
    interpolate: /\{\{(.+?)\}\}/g,
    evaluate:    /\{\%(.+?)\%\}/g,          
    // interpolate: /\{\{=(.+?)\}\}/g,
    escape: /\{\{-(.+?)\}\}/g
};

var editors = {};

function configureEditor(id) 
{



    // configure ace editor
    var editor = ace.edit(id);
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");
    editor.getSession().setUseWrapMode(true);
    editor.getSession().setUseSoftTabs(true);
    editor.getSession().setNewLineMode("unix");
    editor.renderer.setShowGutter(true); 

    editors[id] = editor;

    return editor;
}



function initEditors()
{

    if($("#user-code").length)
    {
        var userCodeEditor = configureEditor("user-code");
    }

    if($("#response-editor").length)
    {
        configureEditor("response-editor");
        var mainHeight = $(window).height();
        mainHeight -= $('#top-header').height();
        mainHeight -= $('#bottom-footer').height();
        mainHeight -= 80;

        $('#response-editor').height(mainHeight);
    }

    if($("#prompt-editor").length)
    {
        var prompt = configureEditor("prompt-editor");
        prompt.getSession().setMode("ace/mode/markdown");   

        configureEditor("solution-editor");

        $("#save-question").click(function (event) 
        {
            submitQuestion();
        });
    }
}

/**
 * Copy the from ace editor into a hidden filed to 
 * submit user-generated code
 */
function copyEditorCode(id)
{
    var codeField = $("#" + id).data("codeField");
    var editor = editors[id];
    var code = editor.getValue();
    $("input[name=" + codeField + "]").val(code);
}


function submitQuestion(e)
{
    if(e)
        e.preventDefault();

    copyEditorCode("prompt-editor");
    copyEditorCode("solution-editor");

    var $form = $("#question-form");
    var data = $form.serialize();   
    var url = $form.attr( "action" );

    $.post( url, data ).success(function( response ) 
    {
        question.set(JSON.parse(response.question));
        message.set(response.msg);
        editors["solution-editor"].focus();
        // alert("need to update tests...todo");
    });

}

msg = function(msg, level)
{
    var html = $('#msg-li-tmpl').html();
    var tmpl = _.template(html);
    var alert = tmpl({msg: msg, level: level});
    $( '#messages' ).append(alert);
    var clear = function() { $( '#messages' ).html(''); }
    _.delay(clear, 3000);
}

function submitTestForm(e)
{

    e.preventDefault();
    if (question.id == 0)
    {
        msg("You must save your function name and prompt before adding tests.", danger);
    }
    else
    {

        var $form = $( this );
        var data = $form.serialize();   
        var url = $form.attr( "action" );

        $.post( url, data ).success(function( response ) 
        {

            if ( response.success )
            {
                TestResults.add(JSON.parse(response.tests_json));
                question.set(JSON.parse(response.question_json));
                message.set(response.message);
            }
            else
            {
                msg(response.msg, 'danger');
            }
        });
    }
}



function submitStudyCode(action)
{

    // Stop form from submitting normally
    //e.preventDefault();


    copyEditorCode("response-editor");

    var $form = $("#response-form");
    var data = $form.serialize() + "&action=" + action;   
    var url = $form.attr( "action" );

    $.post( url, data ).success(function( response ) 
    {

        $( "#test-results" ).html( response );
        editors["response-editor"].focus();
    });

}


/**
 * A client-side post-fix for the ugly diff
 * table that python provides
 */
function fixDiff()
{
    var tables = $("table.diff");
    $(tables).removeAttr("cellpadding");
    $(tables).removeAttr("cellspacing");
    $(tables).removeAttr("rules");
    $(tables).addClass("table table-condensed table-bordered table-hover");
    $("table.diff colgroup").remove();
    $("table.diff td").removeAttr("nowrap");
    $("td.diff_next").remove();
}

function showQuestionDetails(e)
{
    questionId = $(e.target).data("quid");
    url = "/study/question_detail/" + questionId
    // this actually goes to the /study/question_detail/___ function
    // in student_views.py.
    // that function returns the question_detail.html template
    $.get(url, function( data ) {
        // instead of redirecting to the question_detail page,
        // take that page's HTML and put it inside the
        // #question-details row.
        $("#question-details").html( data );
        $("#question-details").removeClass('hidden');
    });

}

function changeLevel(level, description)
{

  $("#question-details").addClass("hidden");
  $("#current-level").html(" Current Level: " + level + " - " + description);
  $(".question-row").each(function()
  {
    if (level != $(this).data("level"))
    {
      // hide this level
      $(this).addClass("hidden");
    }
    else {
      $(this).removeClass("hidden");
    }
  });
  return;

}

function makeButton(link, text, type)
{
    var btn = $("a");
    a.addClass("btn");
    a.addClass("btn-"+type);
    a.html(text);
    a.attr("href", "link");

}


function initForms()
{
    $("form").each(function()
    {
        var f = this;
        if($(f).find(".change-indicator").length > 0)
        {
            var formState = $(f).find(".change-indicator");
            var showChange = function() 
            { 
                $(formState).removeClass("label-success").addClass("label-warning");
            }
            $(f).find("select, checkbox, radio").on("change", showChange);
            $(f).find("input, select, checkbox, radio, textarea").on("input", showChange);
        }

    });

}

$( document ).ready(function() {

    var tips = $("*[data-toggle='tooltip']");
    $(tips).popover({ container: 'body', trigger: 'hover', delay: { "show": 500, "hide": 100 } });


    fixDiff();
    initEditors();
    initForms();

   //question form stuff
    $( "#test-form" ).submit(submitTestForm);
    
    if($( "#question-form" ).length)
    {

        var prompt = editors["prompt-editor"];
        var solution = editors["solution-editor"];


        _.each([prompt, solution], function(editor)
        {
            editor.commands.addCommand({
                name: "save",
                bindKey: 
                {
                    win: 'Ctrl-S',
                    mac: 'Command-S',
                    sender: 'editor|cli'
                },                
                exec: function(env, args, request) { submitQuestion(); }
            });
        });
    }


    var runUserFunction = function() {submitStudyCode("run"); return false;}
    $( "#run-code" ).click(runUserFunction);
    
    // var testUserFunction = function(e) {submitStudyCode(e, "test");}
    // $( "#test-code" ).click(testUserFunction);
    if($( "#run-code" ).length > 0)
    {
        var editor = editors["response-editor"];
        editor.focus();
        editor.gotoLine(3);

        editor.commands.addCommand({
            name: "build",
            bindKey: {win: "Ctrl-B", mac: "Command-B"},
            exec: function(editor) { runUserFunction(); }
        });

        editor.commands.addCommand({
            name: "skip",
            bindKey: {win: "Ctrl-K", mac: "Command-K"},
            exec: function(editor) { window.location = "/tutor"; }
        });

    }

    $("#passed-modal").keypress(function( event ) {
        if ( event.which == 13 && $(".modal a.enter")) 
        {
            event.preventDefault();
            var target = $(".modal a.enter").attr('href');
            window.location = target;
            return;
        }
    });

    $("#question-edit-tabs a").click(function (e) {
        $(this).tab('show');
    });

    $(".form-group select, .form-group input").addClass("form-control");

    $( "#id_comment").val("");


    TableSorter.init();


    $(".question_detail").click(showQuestionDetails)

    $('.change-level').click(function (e) {
        var level = $(this).data("level");
        var description = $(this).data("description");
        changeLevel(level, description);
    });

    if ($("#current-level").length > 0)
    {
        current_info = $("#current-level")[0];
        var level = $(current_info).data("level");
        var description = $(current_info).data("description");
        changeLevel(level, description);
    }

});
