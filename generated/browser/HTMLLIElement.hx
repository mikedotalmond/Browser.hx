//
// Browser.hx - JS externs for Haxe
// https://github.com/aduros/Browser.hx/blob/master/LICENSE.txt
//
// This file is generated, do not edit!

package browser;

/** The <em>HTML List item element</em> (<code>&lt;li&gt;</code>) is used to represent a list item. It should be contained in an ordered list (<code><a rel="custom" href="https://developer.mozilla.org/en/HTML/Element/ol">&lt;ol&gt;</a></code>
), an unordered list (<code><a rel="custom" href="https://developer.mozilla.org/en/HTML/Element/ul">&lt;ul&gt;</a></code>
) or a menu (<code><a rel="custom" href="https://developer.mozilla.org/en/HTML/Element/menu">&lt;menu&gt;</a></code>
), where it represents a single entity in that list. In menus and unordered lists, list items are ordinarily displayed using bullet points. In order lists, they are usually displayed with some ascending counter on the left such as a number or letter<br><br>
Documentation for this class was provided by <a href="https://developer.mozilla.org/en/HTML/Element/li">MDN</a>. */
@:native("HTMLLIElement")
extern class HTMLLIElement extends HTMLElement
{
    /** This character attributes indicates the numbering type: <ul> <li><code>a</code>: lowercase letters</li> <li><code>A</code>: uppercase letters</li> <li><code>i</code>: lowercase Roman numerals</li> <li><code>I</code>: uppercase Roman numerals</li> <li><code>1</code>: numbers</li> </ul> This type overrides the one used by its parent <code><a rel="custom" href="https://developer.mozilla.org/en/HTML/Element/ol">&lt;ol&gt;</a></code>
 element, if any.<br> <div class="note"><strong>Usage note:</strong> This attribute has been deprecated: use the CSS <code><a rel="custom" href="https://developer.mozilla.org/en/CSS/list-style-type">list-style-type</a></code>
 property instead.</div> */
    var type :String;

    /** This integer attributes indicates the current ordinal value of the item in the list as defined by the <code><a rel="custom" href="https://developer.mozilla.org/en/HTML/Element/ol">&lt;ol&gt;</a></code>
 element. The only allowed value for this attribute is a number, even if the list is displayed with Roman numerals or letters. List items that follow this one continue numbering from the value set. The <strong>value</strong> attribute has no meaning for unordered lists (<code><a rel="custom" href="https://developer.mozilla.org/en/HTML/Element/ul">&lt;ul&gt;</a></code>
) or for menus (<code><a rel="custom" href="https://developer.mozilla.org/en/HTML/Element/menu">&lt;menu&gt;</a></code>
). <div class="note"><strong>Note</strong>: This attribute was deprecated in HTML4, but reintroduced in HTML5.</div> <div class="geckoVersionNote"> <p>
</p><div class="geckoVersionHeading">Gecko 9.0 note<div>(Firefox 9.0 / Thunderbird 9.0 / SeaMonkey 2.6)
</div></div>
<p></p> <p>Prior to <span title="(Firefox 9.0 / Thunderbird 9.0 / SeaMonkey 2.6)
">Gecko&nbsp;9.0</span>, negative values were incorrectly converted to 0. Starting in <span title="(Firefox 9.0 / Thunderbird 9.0 / SeaMonkey 2.6)
">Gecko&nbsp;9.0</span> all integer values are correctly parsed.</p> </div> */
    var value :Int;

}
