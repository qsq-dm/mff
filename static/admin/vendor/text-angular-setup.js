/*
@license textAngular
Author : Austin Anderson
License : 2013 MIT
Version 1.3.7

See README.md or https://github.com/fraywing/textAngular/wiki for requirements and use.
*/
angular.module('textAngularSetup', [])

// Here we set up the global display defaults, to set your own use a angular $provider#decorator.
.value('taOptions', {
    toolbar: [
        ['h1', 'h2', 'h3', 'p', 'quote'],
        ['bold', 'italics', 'underline', 'strikeThrough', 'ul', 'ol', 'redo', 'undo', 'clear'],
        ['justifyLeft', 'justifyCenter', 'justifyRight', 'insertLink', 'insertImage'],
        ['backgroundColor', 'fontColor'],
        ['fontSize', 'fontName']
    ],
    classes: {
        focussed: "focussed",
        toolbar: "btn-toolbar",
        toolbarGroup: "btn-group",
        toolbarButton: "btn btn-blue",
        toolbarButtonActive: "active",
        disabled: "disabled",
        textEditor: 'form-control',
        htmlEditor: 'form-control'
    },
    defaultTagAttributes: {
        a: { target: "" }
    },
    setup: {
        // wysiwyg mode
        textEditorSetup: function ($element) { /* Do some processing here */ },
        // raw html
        htmlEditorSetup: function ($element) { /* Do some processing here */ }
    },
    defaultFileDropHandler:
		/* istanbul ignore next: untestable image processing */
		function (file, insertAction) {
		    var reader = new FileReader();
		    if (file.type.substring(0, 5) === 'image') {
		        reader.onload = function () {
		            if (reader.result !== '') insertAction('insertImage', reader.result, true);
		        };

		        reader.readAsDataURL(file);
		        // NOTE: For async procedures return a promise and resolve it when the editor should update the model.
		        return true;
		    }
		    return false;
		}
})

// This is the element selector string that is used to catch click events within a taBind, prevents the default and $emits a 'ta-element-select' event
// these are individually used in an angular.element().find() call. What can go here depends on whether you have full jQuery loaded or just jQLite with angularjs.
// div is only used as div.ta-insert-video caught in filter.
.value('taSelectableElements', ['a', 'img'])

// This is an array of objects with the following options:
//				selector: <string> a jqLite or jQuery selector string
//				customAttribute: <string> an attribute to search for
//				renderLogic: <function(element)>
// Both or one of selector and customAttribute must be defined.
.value('taCustomRenderers', [
	{
	    // Parse back out: '<div class="ta-insert-video" ta-insert-video src="' + urlLink + '" allowfullscreen="true" width="300" frameborder="0" height="250"></div>'
	    // To correct video element. For now only support youtube
	    selector: 'img',
	    customAttribute: 'ta-insert-video',
	    renderLogic: function (element) {
	        var iframe = angular.element('<iframe></iframe>');
	        var attributes = element.prop("attributes");
	        // loop through element attributes and apply them on iframe
	        angular.forEach(attributes, function (attr) {
	            iframe.attr(attr.name, attr.value);
	        });
	        iframe.attr('src', iframe.attr('ta-insert-video'));
	        element.replaceWith(iframe);
	    }
	}
])

.value('taTranslations', {
    // moved to sub-elements
    //toggleHTML: "Toggle HTML",
    //insertImage: "Please enter a image URL to insert",
    //insertLink: "Please enter a URL to insert",
    //insertVideo: "Please enter a youtube URL to embed",
    html: {
        tooltip: 'Toggle html / Rich Text'
    },
    // tooltip for heading - might be worth splitting
    heading: {
        tooltip: 'Heading '
    },
    p: {
        tooltip: 'paragraph'
    },
    pre: {
        tooltip: 'Preformmatted text'
    },
    ul: {
        tooltip: '无索引列表'
    },
    ol: {
        tooltip: '索引列表'
    },
    quote: {
        tooltip: '引用段落'
    },
    undo: {
        tooltip: '撤销'
    },
    redo: {
        tooltip: '恢复'
    },
    bold: {
        tooltip: '加粗'
    },
    italic: {
        tooltip: '斜体'
    },
    underline: {
        tooltip: '下划线'
    },
    strikeThrough: {
        tooltip: '横线'
    },
    justifyLeft: {
        tooltip: '左对齐'
    },
    justifyRight: {
        tooltip: '右对齐'
    },
    justifyCenter: {
        tooltip: '居中'
    },
    indent: {
        tooltip: 'Increase indent'
    },
    outdent: {
        tooltip: 'Decrease indent'
    },
    clear: {
        tooltip: '清除格式'
    },
    insertImage: {
        dialogPrompt: '插入图片',
        tooltip: '插入图片',
        hotkey: 'the - possibly language dependent hotkey ... for some future implementation'
    },
    insertVideo: {
        tooltip: 'Insert video',
        dialogPrompt: 'Please enter a youtube URL to embed'
    },
    insertLink: {
        tooltip: 'Insert / edit link',
        dialogPrompt: "Por favor introduzca una URL"
    },
    editLink: {
        reLinkButton: {
            tooltip: "Reescribir link"
        },
        unLinkButton: {
            tooltip: "Quitar link"
        },
        targetToggle: {
            buttontext: "Open in New Window"
        }
    },
    wordcount: {
        tooltip: 'Display words Count'
    },
    charcount: {
        tooltip: 'Display characters Count'
    }
})
.run(['taRegisterTool', '$window', 'taTranslations', 'taSelection', function (taRegisterTool, $window, taTranslations, taSelection) {
    taRegisterTool("html", {
        iconclass: 'fa fa-code',
        tooltiptext: taTranslations.html.tooltip,
        action: function () {
            this.$editor().switchView();
        },
        activeState: function () {
            return this.$editor().showHtml;
        }
    });
    // add the Header tools
    // convenience functions so that the loop works correctly
    var _retActiveStateFunction = function (q) {
        return function () { return this.$editor().queryFormatBlockState(q); };
    };
    var headerAction = function () {
        return this.$editor().wrapSelection("formatBlock", "<" + this.name.toUpperCase() + ">");
    };
    angular.forEach(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], function (h) {
        taRegisterTool(h.toLowerCase(), {
            buttontext: h.toUpperCase(),
            tooltiptext: taTranslations.heading.tooltip + h.charAt(1),
            action: headerAction,
            activeState: _retActiveStateFunction(h.toLowerCase())
        });
    });
    taRegisterTool('p', {
        buttontext: 'P',
        tooltiptext: taTranslations.p.tooltip,
        action: function () {
            return this.$editor().wrapSelection("formatBlock", "<P>");
        },
        activeState: function () { return this.$editor().queryFormatBlockState('p'); }
    });
    // key: pre -> taTranslations[key].tooltip, taTranslations[key].buttontext
    taRegisterTool('pre', {
        buttontext: 'pre',
        tooltiptext: taTranslations.pre.tooltip,
        action: function () {
            return this.$editor().wrapSelection("formatBlock", "<PRE>");
        },
        activeState: function () { return this.$editor().queryFormatBlockState('pre'); }
    });
    taRegisterTool('ul', {
        iconclass: 'fa fa-list-ul',
        tooltiptext: taTranslations.ul.tooltip,
        action: function () {
            return this.$editor().wrapSelection("insertUnorderedList", null);
        },
        activeState: function () { return this.$editor().queryCommandState('insertUnorderedList'); }
    });
    taRegisterTool('ol', {
        iconclass: 'fa fa-list-ol',
        tooltiptext: taTranslations.ol.tooltip,
        action: function () {
            return this.$editor().wrapSelection("insertOrderedList", null);
        },
        activeState: function () { return this.$editor().queryCommandState('insertOrderedList'); }
    });
    taRegisterTool('quote', {
        iconclass: 'fa fa-quote-right',
        tooltiptext: taTranslations.quote.tooltip,
        action: function () {
            return this.$editor().wrapSelection("formatBlock", "<BLOCKQUOTE>");
        },
        activeState: function () { return this.$editor().queryFormatBlockState('blockquote'); }
    });
    taRegisterTool('undo', {
        iconclass: 'fa fa-undo',
        tooltiptext: taTranslations.undo.tooltip,
        action: function () {
            return this.$editor().wrapSelection("undo", null);
        }
    });
    taRegisterTool('redo', {
        iconclass: 'fa fa-repeat',
        tooltiptext: taTranslations.redo.tooltip,
        action: function () {
            return this.$editor().wrapSelection("redo", null);
        }
    });
    taRegisterTool('bold', {
        iconclass: 'fa fa-bold',
        tooltiptext: taTranslations.bold.tooltip,
        action: function () {
            return this.$editor().wrapSelection("bold", null);
        },
        activeState: function () {
            return this.$editor().queryCommandState('bold');
        },
        commandKeyCode: 98
    });
    taRegisterTool('justifyLeft', {
        iconclass: 'fa fa-align-left',
        tooltiptext: taTranslations.justifyLeft.tooltip,
        action: function () {
            return this.$editor().wrapSelection("justifyLeft", null);
        },
        activeState: function (commonElement) {
            var result = false;
            if (commonElement) result =
				commonElement.css('text-align') === 'left' ||
				commonElement.attr('align') === 'left' ||
				(
					commonElement.css('text-align') !== 'right' &&
					commonElement.css('text-align') !== 'center' &&
					commonElement.css('text-align') !== 'justify' &&
					!this.$editor().queryCommandState('justifyRight') &&
					!this.$editor().queryCommandState('justifyCenter')
				) && !this.$editor().queryCommandState('justifyFull');
            result = result || this.$editor().queryCommandState('justifyLeft');
            return result;
        }
    });
    taRegisterTool('justifyRight', {
        iconclass: 'fa fa-align-right',
        tooltiptext: taTranslations.justifyRight.tooltip,
        action: function () {
            return this.$editor().wrapSelection("justifyRight", null);
        },
        activeState: function (commonElement) {
            var result = false;
            if (commonElement) result = commonElement.css('text-align') === 'right';
            result = result || this.$editor().queryCommandState('justifyRight');
            return result;
        }
    });
    taRegisterTool('justifyCenter', {
        iconclass: 'fa fa-align-center',
        tooltiptext: taTranslations.justifyCenter.tooltip,
        action: function () {
            return this.$editor().wrapSelection("justifyCenter", null);
        },
        activeState: function (commonElement) {
            var result = false;
            if (commonElement) result = commonElement.css('text-align') === 'center';
            result = result || this.$editor().queryCommandState('justifyCenter');
            return result;
        }
    });
    taRegisterTool('indent', {
        iconclass: 'fa fa-indent',
        tooltiptext: taTranslations.indent.tooltip,
        action: function () {
            return this.$editor().wrapSelection("indent", null);
        },
        activeState: function () {
            return this.$editor().queryFormatBlockState('blockquote');
        }
    });
    taRegisterTool('outdent', {
        iconclass: 'fa fa-outdent',
        tooltiptext: taTranslations.outdent.tooltip,
        action: function () {
            return this.$editor().wrapSelection("outdent", null);
        },
        activeState: function () {
            return false;
        }
    });
    taRegisterTool('italics', {
        iconclass: 'fa fa-italic',
        tooltiptext: taTranslations.italic.tooltip,
        action: function () {
            return this.$editor().wrapSelection("italic", null);
        },
        activeState: function () {
            return this.$editor().queryCommandState('italic');
        },
        commandKeyCode: 105
    });
    taRegisterTool('underline', {
        iconclass: 'fa fa-underline',
        tooltiptext: taTranslations.underline.tooltip,
        action: function () {
            return this.$editor().wrapSelection("underline", null);
        },
        activeState: function () {
            return this.$editor().queryCommandState('underline');
        },
        commandKeyCode: 117
    });
    taRegisterTool('strikeThrough', {
        iconclass: 'fa fa-strikethrough',
        tooltiptext: taTranslations.strikeThrough.tooltip,
        action: function () {
            return this.$editor().wrapSelection("strikeThrough", null);
        },
        activeState: function () {
            return document.queryCommandState('strikeThrough');
        }
    });
    taRegisterTool('clear', {
        iconclass: 'fa fa-ban',
        tooltiptext: taTranslations.clear.tooltip,
        action: function (deferred, restoreSelection) {
            var i;
            this.$editor().wrapSelection("removeFormat", null);
            var possibleNodes = angular.element(taSelection.getSelectionElement());
            // remove lists
            var removeListElements = function (list) {
                list = angular.element(list);
                var prevElement = list;
                angular.forEach(list.children(), function (liElem) {
                    var newElem = angular.element('<p></p>');
                    newElem.html(angular.element(liElem).html());
                    prevElement.after(newElem);
                    prevElement = newElem;
                });
                list.remove();
            };
            angular.forEach(possibleNodes.find("ul"), removeListElements);
            angular.forEach(possibleNodes.find("ol"), removeListElements);
            if (possibleNodes[0].tagName.toLowerCase() === 'li') {
                var _list = possibleNodes[0].parentNode.childNodes;
                var _preLis = [], _postLis = [], _found = false;
                for (i = 0; i < _list.length; i++) {
                    if (_list[i] === possibleNodes[0]) {
                        _found = true;
                    } else if (!_found) _preLis.push(_list[i]);
                    else _postLis.push(_list[i]);
                }
                var _parent = angular.element(possibleNodes[0].parentNode);
                var newElem = angular.element('<p></p>');
                newElem.html(angular.element(possibleNodes[0]).html());
                if (_preLis.length === 0 || _postLis.length === 0) {
                    if (_postLis.length === 0) _parent.after(newElem);
                    else _parent[0].parentNode.insertBefore(newElem[0], _parent[0]);

                    if (_preLis.length === 0 && _postLis.length === 0) _parent.remove();
                    else angular.element(possibleNodes[0]).remove();
                } else {
                    var _firstList = angular.element('<' + _parent[0].tagName + '></' + _parent[0].tagName + '>');
                    var _secondList = angular.element('<' + _parent[0].tagName + '></' + _parent[0].tagName + '>');
                    for (i = 0; i < _preLis.length; i++) _firstList.append(angular.element(_preLis[i]));
                    for (i = 0; i < _postLis.length; i++) _secondList.append(angular.element(_postLis[i]));
                    _parent.after(_secondList);
                    _parent.after(newElem);
                    _parent.after(_firstList);
                    _parent.remove();
                }
                taSelection.setSelectionToElementEnd(newElem[0]);
            }
            // clear out all class attributes. These do not seem to be cleared via removeFormat
            var $editor = this.$editor();
            var recursiveRemoveClass = function (node) {
                node = angular.element(node);
                if (node[0] !== $editor.displayElements.text[0]) node.removeAttr('class');
                angular.forEach(node.children(), recursiveRemoveClass);
            };
            angular.forEach(possibleNodes, recursiveRemoveClass);
            // check if in list. If not in list then use formatBlock option
            if (possibleNodes[0].tagName.toLowerCase() !== 'li' &&
				possibleNodes[0].tagName.toLowerCase() !== 'ol' &&
				possibleNodes[0].tagName.toLowerCase() !== 'ul') this.$editor().wrapSelection("formatBlock", "default");
            restoreSelection();
        }
    });

    var imgOnSelectAction = function (event, $element, editorScope) {
        // setup the editor toolbar
        // Credit to the work at http://hackerwins.github.io/summernote/ for this editbar logic/display
        var finishEdit = function () {
            editorScope.updateTaBindtaTextElement();
            editorScope.hidePopover();
        };
        event.preventDefault();
        editorScope.displayElements.popover.css('width', '375px');
        var container = editorScope.displayElements.popoverContainer;
        container.empty();
        var buttonGroup = angular.element('<div class="btn-group" style="padding-right: 6px;">');
        var fullButton = angular.element('<button type="button" class="btn btn-default btn-sm btn-small" unselectable="on" tabindex="-1">100% </button>');
        fullButton.on('click', function (event) {
            event.preventDefault();
            $element.css({
                'width': '100%',
                'height': ''
            });
            finishEdit();
        });
        var halfButton = angular.element('<button type="button" class="btn btn-default btn-sm btn-small" unselectable="on" tabindex="-1">50% </button>');
        halfButton.on('click', function (event) {
            event.preventDefault();
            $element.css({
                'width': '50%',
                'height': ''
            });
            finishEdit();
        });
        var quartButton = angular.element('<button type="button" class="btn btn-default btn-sm btn-small" unselectable="on" tabindex="-1">25% </button>');
        quartButton.on('click', function (event) {
            event.preventDefault();
            $element.css({
                'width': '25%',
                'height': ''
            });
            finishEdit();
        });
        var resetButton = angular.element('<button type="button" class="btn btn-default btn-sm btn-small" unselectable="on" tabindex="-1">Reset</button>');
        resetButton.on('click', function (event) {
            event.preventDefault();
            $element.css({
                width: '',
                height: ''
            });
            finishEdit();
        });
        buttonGroup.append(fullButton);
        buttonGroup.append(halfButton);
        buttonGroup.append(quartButton);
        buttonGroup.append(resetButton);
        container.append(buttonGroup);

        buttonGroup = angular.element('<div class="btn-group" style="padding-right: 6px;">');
        var floatLeft = angular.element('<button type="button" class="btn btn-default btn-sm btn-small" unselectable="on" tabindex="-1"><i class="fa fa-align-left"></i></button>');
        floatLeft.on('click', function (event) {
            event.preventDefault();
            // webkit
            $element.css('float', 'left');
            // firefox
            $element.css('cssFloat', 'left');
            // IE < 8
            $element.css('styleFloat', 'left');
            finishEdit();
        });
        var floatRight = angular.element('<button type="button" class="btn btn-default btn-sm btn-small" unselectable="on" tabindex="-1"><i class="fa fa-align-right"></i></button>');
        floatRight.on('click', function (event) {
            event.preventDefault();
            // webkit
            $element.css('float', 'right');
            // firefox
            $element.css('cssFloat', 'right');
            // IE < 8
            $element.css('styleFloat', 'right');
            finishEdit();
        });
        var floatNone = angular.element('<button type="button" class="btn btn-default btn-sm btn-small" unselectable="on" tabindex="-1"><i class="fa fa-align-justify"></i></button>');
        floatNone.on('click', function (event) {
            event.preventDefault();
            // webkit
            $element.css('float', '');
            // firefox
            $element.css('cssFloat', '');
            // IE < 8
            $element.css('styleFloat', '');
            finishEdit();
        });
        buttonGroup.append(floatLeft);
        buttonGroup.append(floatNone);
        buttonGroup.append(floatRight);
        container.append(buttonGroup);

        buttonGroup = angular.element('<div class="btn-group">');
        var remove = angular.element('<button type="button" class="btn btn-default btn-sm btn-small" unselectable="on" tabindex="-1"><i class="fa fa-trash-o"></i></button>');
        remove.on('click', function (event) {
            event.preventDefault();
            $element.remove();
            finishEdit();
        });
        buttonGroup.append(remove);
        container.append(buttonGroup);

        editorScope.showPopover($element);
        editorScope.showResizeOverlay($element);
    };

    taRegisterTool('insertImage', {
        iconclass: 'fa fa-picture-o',
        tooltiptext: taTranslations.insertImage.tooltip,
        action: function () {
            var imageLink;
            imageLink = $window.prompt(taTranslations.insertImage.dialogPrompt, 'http://');
            if (imageLink && imageLink !== '' && imageLink !== 'http://') {
                return this.$editor().wrapSelection('insertImage', imageLink, true);
            }
        },
        onElementSelect: {
            element: 'img',
            action: imgOnSelectAction
        }
    });
    taRegisterTool('insertVideo', {
        iconclass: 'fa fa-youtube-play',
        tooltiptext: taTranslations.insertVideo.tooltip,
        action: function () {
            var urlPrompt;
            urlPrompt = $window.prompt(taTranslations.insertVideo.dialogPrompt, 'https://');
            if (urlPrompt && urlPrompt !== '' && urlPrompt !== 'https://') {
                // get the video ID
                var ids = urlPrompt.match(/(\?|&)v=[^&]*/);
                /* istanbul ignore else: if it's invalid don't worry - though probably should show some kind of error message */
                if (ids && ids.length > 0) {
                    // create the embed link
                    var urlLink = "https://www.youtube.com/embed/" + ids[0].substring(3);
                    // create the HTML
                    // for all options see: http://stackoverflow.com/questions/2068344/how-do-i-get-a-youtube-video-thumbnail-from-the-youtube-api
                    // maxresdefault.jpg seems to be undefined on some.
                    var embed = '<img class="ta-insert-video" src="https://img.youtube.com/vi/' + ids[0].substring(3) + '/hqdefault.jpg" ta-insert-video="' + urlLink + '" contenteditable="false" allowfullscreen="true" frameborder="0" />';
                    // insert
                    return this.$editor().wrapSelection('insertHTML', embed, true);
                }
            }
        },
        onElementSelect: {
            element: 'img',
            onlyWithAttrs: ['ta-insert-video'],
            action: imgOnSelectAction
        }
    });
    taRegisterTool('insertLink', {
        tooltiptext: taTranslations.insertLink.tooltip,
        iconclass: 'fa fa-link',
        action: function () {
            var urlLink;
            urlLink = $window.prompt(taTranslations.insertLink.dialogPrompt, 'http://');
            if (urlLink && urlLink !== '' && urlLink !== 'http://') {
                return this.$editor().wrapSelection('createLink', urlLink, true);
            }
        },
        activeState: function (commonElement) {
            if (commonElement) return commonElement[0].tagName === 'A';
            return false;
        },
        onElementSelect: {
            element: 'a',
            action: function (event, $element, editorScope) {
                // setup the editor toolbar
                // Credit to the work at http://hackerwins.github.io/summernote/ for this editbar logic
                event.preventDefault();
                editorScope.displayElements.popover.css('width', '436px');
                var container = editorScope.displayElements.popoverContainer;
                container.empty();
                container.css('line-height', '28px');
                var link = angular.element('<a href="' + $element.attr('href') + '" target="_blank">' + $element.attr('href') + '</a>');
                link.css({
                    'display': 'inline-block',
                    'max-width': '325px',
                    'overflow': 'hidden',
                    'text-overflow': 'ellipsis',
                    'white-space': 'nowrap',
                    'vertical-align': 'middle'
                });
                container.append(link);
                var buttonGroup = angular.element('<div class="btn-group pull-right">');
                var reLinkButton = angular.element('<button type="button" class="btn btn-blue btn-sm btn-small" tabindex="-1" unselectable="on" title="' + taTranslations.editLink.reLinkButton.tooltip + '"><i class="fa fa-edit"></i></button>');
                reLinkButton.on('click', function (event) {
                    event.preventDefault();
                    var urlLink = $window.prompt(taTranslations.insertLink.dialogPrompt, $element.attr('href'));
                    if (urlLink && urlLink !== '' && urlLink !== 'http://') {
                        $element.attr('href', urlLink);
                        editorScope.updateTaBindtaTextElement();
                    }
                    editorScope.hidePopover();
                });
                buttonGroup.append(reLinkButton);
                var unLinkButton = angular.element('<button type="button" class="btn btn-blue btn-sm btn-small" tabindex="-1" unselectable="on" title="' + taTranslations.editLink.unLinkButton.tooltip + '"><i class="fa fa-unlink"></i></button>');
                // directly before this click event is fired a digest is fired off whereby the reference to $element is orphaned off
                unLinkButton.on('click', function (event) {
                    event.preventDefault();
                    $element.replaceWith($element.contents());
                    editorScope.updateTaBindtaTextElement();
                    editorScope.hidePopover();
                });
                buttonGroup.append(unLinkButton);
                var targetToggle = angular.element('<button type="button" class="btn btn-blue btn-sm btn-small" tabindex="-1" unselectable="on">' + taTranslations.editLink.targetToggle.buttontext + '</button>');
                if ($element.attr('target') === '_blank') {
                    targetToggle.addClass('active');
                }
                targetToggle.on('click', function (event) {
                    event.preventDefault();
                    $element.attr('target', ($element.attr('target') === '_blank') ? '' : '_blank');
                    targetToggle.toggleClass('active');
                    editorScope.updateTaBindtaTextElement();
                });
                //buttonGroup.append(targetToggle);
                container.append(buttonGroup);
                editorScope.showPopover($element);
            }
        }
    });
    taRegisterTool('wordcount', {
        display: '<div id="toolbarWC" style="display:block; min-width:100px;">Palabras: <span ng-bind="wordcount"></span></div>',
        disabled: true,
        wordcount: 0,
        activeState: function () { // this fires on keyup
            var textElement = this.$editor().displayElements.text;
            /* istanbul ignore next: will default to '' when undefined */
            var workingHTML = textElement[0].innerHTML || '';
            var noOfWords = 0;

            /* istanbul ignore if: will default to '' when undefined */
            if (workingHTML.replace(/\s*<[^>]*?>\s*/g, '') !== '') {
                noOfWords = workingHTML.replace(/<\/?(b|i|em|strong|span|u|strikethrough|a|img|small|sub|sup|label)( [^>*?])?>/gi, '') // remove inline tags without adding spaces
										.replace(/(<[^>]*?>\s*<[^>]*?>)/ig, ' ') // replace adjacent tags with possible space between with a space
										.replace(/(<[^>]*?>)/ig, '') // remove any singular tags
										.replace(/\s+/ig, ' ') // condense spacing
										.match(/\S+/g).length; // count remaining non-space strings
            }

            //Set current scope
            this.wordcount = noOfWords;
            //Set editor scope
            this.$editor().wordcount = noOfWords;

            return false;
        }
    });
    taRegisterTool('charcount', {
        display: '<div id="toolbarCC" style="display:block; min-width:120px;">Car&aacute;cteres: <span ng-bind="charcount"></span></div>',
        disabled: true,
        charcount: 0,
        activeState: function () { // this fires on keyup
            var textElement = this.$editor().displayElements.text;
            var sourceText = textElement[0].innerText || textElement[0].textContent; // to cover the non-jquery use case.

            // Caculate number of chars
            var noOfChars = sourceText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, ' ').replace(/\s+$/g, ' ').length;
            //Set current scope
            this.charcount = noOfChars;
            //Set editor scope
            this.$editor().charcount = noOfChars;
            return false;
        }
    });

    taRegisterTool('fontName', {
        display: "<span class='bar-btn-dropdown dropdown'>" +
                "<button class='btn btn-blue dropdown-toggle' type='button' ng-disabled='showHtml()' style='padding-top: 4px'><i class='fa fa-font'></i><i class='fa fa-caret-down'></i></button>" +
                "<ul class='dropdown-menu'><li ng-repeat='o in options'><button class='btn btn-blue checked-dropdown' style='font-family: {{o.css}}; width: 100%' type='button' ng-click='action($event, o.css)'><i ng-if='o.active' class='fa fa-check'></i>{{o.name}}</button></li></ul></span>",
        action: function (event, font) {
            //Ask if event is really an event.
            if (!!event.stopPropagation) {
                //With this, you stop the event of textAngular.
                event.stopPropagation();
                //Then click in the body to close the dropdown.
                $("body").trigger("click");
            }
            return this.$editor().wrapSelection('fontName', font);
        },
        options: [
            { name: 'Sans-Serif', css: 'Arial, Helvetica, sans-serif' },
            { name: 'Serif', css: "'times new roman', serif" },
            { name: 'Wide', css: "'arial black', sans-serif" },
            { name: 'Narrow', css: "'arial narrow', sans-serif" },
            { name: 'Comic Sans MS', css: "'comic sans ms', sans-serif" },
            { name: 'Courier New', css: "'courier new', monospace" },
            { name: 'Garamond', css: 'garamond, serif' },
            { name: 'Georgia', css: 'georgia, serif' },
            { name: 'Tahoma', css: 'tahoma, sans-serif' },
            { name: 'Trebuchet MS', css: "'trebuchet ms', sans-serif" },
            { name: "Helvetica", css: "'Helvetica Neue', Helvetica, Arial, sans-serif" },
            { name: 'Verdana', css: 'verdana, sans-serif' },
            { name: 'Proxima Nova', css: 'proxima_nova_rgregular' }
        ]
    });

    taRegisterTool('fontSize', {
        display: "<span class='bar-btn-dropdown dropdown'>" +
                "<button class='btn btn-blue dropdown-toggle' type='button' ng-disabled='showHtml()' style='padding-top: 4px'><i class='fa fa-text-height'></i><i class='fa fa-caret-down'></i></button>" +
                "<ul class='dropdown-menu'><li ng-repeat='o in options'><button class='btn btn-blue checked-dropdown' style='font-size: {{o.css}}; width: 100%' type='button' ng-click='action($event, o.value)'><i ng-if='o.active' class='fa fa-check'></i> {{o.name}}</button></li></ul>" +
                "</span>",
        action: function (event, size) {
            //Ask if event is really an event.
            if (!!event.stopPropagation) {
                //With this, you stop the event of textAngular.
                event.stopPropagation();
                //Then click in the body to close the dropdown.
                $("body").trigger("click");
            }
            return this.$editor().wrapSelection('fontSize', parseInt(size));
        },
        options: [
            { name: '特小', css: 'xx-small', value: 1 },
            { name: '偏小', css: 'x-small', value: 2 },
            { name: '小', css: 'small', value: 3 },
            { name: '中', css: 'medium', value: 4 },
            { name: '大', css: 'large', value: 5 },
            { name: '偏大', css: 'x-large', value: 6 }
        ]
    });
    taRegisterTool('backgroundColor', {
        display: "<div spectrum-colorpicker ng-model='color' on-change='!!color && action(color)' format='\"hex\"' options='options'></div>",
        action: function (color) {
            var me = this;
            if (!this.$editor().wrapSelection) {
                setTimeout(function () {
                    me.action(color);
                }, 100)
            } else {
                return this.$editor().wrapSelection('backColor', color);
            }
        },
        options: {
            replacerClassName: 'fa fa-paint-brush', showButtons: false
        },
        color: "#fff"
    });
    taRegisterTool('fontColor', {
        display: "<div spectrum-colorpicker ng-model='color' on-change='!!color && action(color)' format='\"hex\"' options='options'></div>",
        action: function (color) {
            var me = this;
            if (!this.$editor().wrapSelection) {
                setTimeout(function () {
                    me.action(color);
                }, 100)
            } else {
                return this.$editor().wrapSelection('foreColor', color);
            }
        },
        options: {
            replacerClassName: 'fa fa-font', showButtons: false
        },
        color: "#000"
    });
}]);
