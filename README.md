# Continued Fraction Streams

This software converts streams of digits to streams of continued fraction coefficients, and vice-versa.

Read my [Continued Fraction Streams](https://x.st/continued-fraction-streams/) writeup to learn more.

## For Example

Next time you forget the digits of the golden ratio, just remember that its continued fraction coefficients are all ones.

…then grab an endless stream of ones from the unexpectedly useful `yes` command:

``` bash
> yes 1
1
1
1
1
1
…
```

…and pipe them into the coefficients-to-digits script:

``` bash
> yes 1 | python3 as_digits.py
1.6180339887498948482045868343656381177203091798057628621354
486227052604628189024497072072041893911374847540880753868917
521266338622235369317931800607667263544333890865959395829056
383226613199282902678806752087668925017116962070322210432162
695486262963136144381497587012203408058879544547492461856953
…
```

This will output a never-ending stream of the digits of the golden ratio.

To check that things are working, you can even pipe the digits back into the digits-to-coefficients script:

``` bash
> yes 1 | python3 as_digits.py | python3 continued_digits.py
1
1
1
1
1
…
```

Cool it works!
