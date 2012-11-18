//
// Browser.hx - JS externs for Haxe
// https://github.com/aduros/Browser.hx/blob/master/LICENSE.txt
//
// This file is generated, do not edit!

package browser;

/** <p><strong>Storage</strong> is a <a class="external" rel="external" href="http://www.sqlite.org/" title="http://www.sqlite.org/" target="_blank">SQLite</a> database API. It is available to trusted callers, meaning extensions and Firefox components only.</p>
<p>The API is currently "unfrozen", which means it is subject to change at any time; in fact, it has changed somewhat with each release of Firefox since it was introduced, and will likely continue to do so for a while.</p>
<div class="note"><strong>Note:</strong> Storage is not the same as the <a title="en/DOM/Storage" rel="internal" href="https://developer.mozilla.org/en/DOM/Storage">DOM:Storage</a> feature which can be used by web pages to store persistent data or the <a title="en/Session_store_API" rel="internal" href="https://developer.mozilla.org/en/Session_store_API">Session store API</a> (an <a title="en/XPCOM" rel="internal" href="https://developer.mozilla.org/en/XPCOM">XPCOM</a> storage utility for use by extensions).</div><br><br>
Documentation for this class was provided by <a href="https://developer.mozilla.org/en/Storage">MDN</a>. */
@:native("Storage")
extern class Storage
{
    /** Getter throws DOMException. */
    var length (default,null) :Int;

    function clear () :Void;

    function getItem (key :String) :String;

    function key (index :Int) :String;

    function removeItem (key :String) :Void;

    function setItem (key :String, data :String) :Void;

}
