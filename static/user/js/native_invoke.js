var standalone = window.navigator.standalone,
    userAgent = window.navigator.userAgent.toLowerCase(),
    safari = /safari/.test( userAgent ),
    ios = /iphone|ipod|ipad/.test( userAgent );
if( ios ) {
    console.log('ios');
    if ( !standalone && safari ) {
        //browser
    } else if ( standalone && !safari ) {
        //standalone
    } else if ( !standalone && !safari ) {
        //uiwebview
    };
} else {
    console.log('android');
};


function GoCreditApply() {

}

function GoCreditResult() {

}

function GoItemDetail(item_id) {

}


function GoItemCats() {

}

