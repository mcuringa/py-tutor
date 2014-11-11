TableSorter = {}

TableSorter.init = function()
{

    var tables = $('.table-sortable');
    var sortableBtnTmpl = _.template($('#th-sort-tmpl').html());

    //go through each header and add a click event
    _.each(tables, function(t) 
    {
        var headers = $(t).find('th');
        _.each(headers, function(header, col) 
        {
            var data = {
                'col': col,
                'header': $(header).html()
            };

            $(header).data("sort", "desc");            
            $(header).html(sortableBtnTmpl(data));
            $(header).click(function(e) {
                TableSorter.sortTable(t, col); 
            });
        });
    });
}

TableSorter.sortTable = function(table, col)
{
    
    //$(header).data("sortDirection", "desc");
    var headers = $(table).find('th');
    var rows = $(table).find('tbody tr');
    var header = headers[col];
    var sortDirection = $(header).data("sort");

    $(headers).removeClass('active');
    $(header).addClass('active');
    $(headers).find('.desc').hide();
    $(headers).find('.asc').hide();


    var sorted = _.sortBy(rows, function(row) 
    {
        var cols = $(row).find('td');
        var html = $(cols[col]).html()
        var sortVal = $(cols[col]).data("sortVal");

        if(_.isUndefined(sortVal) || _.isNull(sortVal) || '' == sortVal)
            sortVal = html;
        
        var sortNum = parseFloat(sortVal);
        if(_.isNaN(sortNum))
        {
            return sortVal;
        }
        return sortNum;
    });

    if("desc" == sortDirection)
    {
        $(header).data("sort", "asc");
        $(header).find('.asc').show();
        $(header).find('.desc').hide();
    }
    else
    {
        sorted.reverse();
        $(header).data("sort", "desc");
        
        $(header).find('.desc').show();
        $(header).find('.asc').hide();
    }
    $(table).find('tbody').html(sorted);    
}