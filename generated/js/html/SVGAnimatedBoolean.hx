//
// Browser.hx - JS externs for Haxe
// https://github.com/aduros/Browser.hx/blob/master/LICENSE.txt
//
// This file is generated, do not edit!

package js.html;

/** The <code>SVGAnimatedBoolean</code> interface is used for attributes of type boolean which can be animated.<br><br>
Documentation for this class was provided by <a href="https://developer.mozilla.org/en/Document_Object_Model_(DOM)/SVGAnimatedBoolean">MDN</a>. */
@:native("SVGAnimatedBoolean")
extern class SVGAnimatedBoolean
{
    /** If the given attribute or property is being animated, contains the current animated value of the attribute or property. If the given attribute or property is not currently being animated, contains the same value as <code>baseVal</code>. */
    var animVal (default,null) :Bool;

    /** The base value of the given attribute before applying any animations. Setter throws DOMException. */
    var baseVal :Bool;

}