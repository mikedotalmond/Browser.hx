//
// Browser.hx - JS externs for Haxe
// https://github.com/aduros/Browser.hx/blob/master/LICENSE.txt
//
// This file is generated, do not edit!

package browser;

/** Refer to <code><a rel="custom" href="https://developer.mozilla.org/en/XPCOM_Interface_Reference/nsIDOMXPathResult">nsIDOMXPathResult</a></code>
 for more detail.<br><br>
Documentation for this class was provided by <a href="https://developer.mozilla.org/en/XPathResult">MDN</a>. */
@:native("XPathResult")
extern class XPathResult
{
    /** A result set containing whatever type naturally results from evaluation of the expression. Note that if the result is a node-set then UNORDERED_NODE_ITERATOR_TYPE is always the resulting type. */
    static inline var ANY_TYPE :Int = 0;

    /** A result node-set containing any single node that matches the expression. The node is not necessarily the first node in the document that matches the expression. */
    static inline var ANY_UNORDERED_NODE_TYPE :Int = 8;

    /** A result containing a single boolean value. This is useful for example, in an XPath expression using the <code>not()</code> function. */
    static inline var BOOLEAN_TYPE :Int = 3;

    /** A result node-set containing the first node in the document that matches the expression. */
    static inline var FIRST_ORDERED_NODE_TYPE :Int = 9;

    /** A result containing a single number. This is useful for example, in an XPath expression using the <code>count()</code> function. */
    static inline var NUMBER_TYPE :Int = 1;

    /** A result node-set containing all the nodes matching the expression. The nodes in the result set are in the same order that they appear in the document. */
    static inline var ORDERED_NODE_ITERATOR_TYPE :Int = 5;

    /** A result node-set containing snapshots of all the nodes matching the expression. The nodes in the result set are in the same order that they appear in the document. */
    static inline var ORDERED_NODE_SNAPSHOT_TYPE :Int = 7;

    /** A result containing a single string. */
    static inline var STRING_TYPE :Int = 2;

    /** A result node-set containing all the nodes matching the expression. The nodes may not necessarily be in the same order that they appear in the document. */
    static inline var UNORDERED_NODE_ITERATOR_TYPE :Int = 4;

    /** A result node-set containing snapshots of all the nodes matching the expression. The nodes may not necessarily be in the same order that they appear in the document. */
    static inline var UNORDERED_NODE_SNAPSHOT_TYPE :Int = 6;

    /** readonly boolean */
    var booleanValue (default,null) :Bool;

    /** readonly boolean */
    var invalidIteratorState (default,null) :Bool;

    /** readonly float */
    var numberValue (default,null) :Float;

    /** readonly integer (short) */
    var resultType (default,null) :Int;

    /** readonly Node */
    var singleNodeValue (default,null) :Node;

    /** readonly Integer */
    var snapshotLength (default,null) :Int;

    /** readonly String */
    var stringValue (default,null) :String;

    function iterateNext () :Node;

    function snapshotItem (index :Int) :Node;

}
