//
// Browser.hx - JS externs for Haxe
// https://github.com/aduros/Browser.hx/blob/master/LICENSE.txt
//
// This file is generated, do not edit!

package browser;

/** The <code>SVGAnimatedAngle</code> interface is used for attributes of basic type <a title="https://developer.mozilla.org/en/SVG/Content_type#Angle" rel="internal" href="https://developer.mozilla.org/en/SVG/Content_type#Angle">&lt;angle&gt;</a> which can be animated.<br><br>
Documentation for this class was provided by <a href="https://developer.mozilla.org/en/DOM/SVGAnimatedAngle">MDN</a>. */
@:native("SVGAnimatedAngle")
extern class SVGAnimatedAngle
{
    /** A read only <code><a rel="custom" href="https://developer.mozilla.org/en/DOM/SVGAngle">SVGAngle</a></code>
 representing the current animated value of the given attribute. If the given attribute is not currently being animated, then the <code><a rel="custom" href="https://developer.mozilla.org/en/DOM/SVGAngle">SVGAngle</a></code>
 will have the same contents as <code>baseVal</code>. The object referenced by <code>animVal</code> will always be distinct from the one referenced by <code>baseVal</code>, even when the attribute is not animated. */
    var animVal (default,null) :SVGAngle;

    /** The base value of the given attribute before applying any animations. */
    var baseVal (default,null) :SVGAngle;

}
