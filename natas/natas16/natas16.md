When it comes to the challenge at this level, it's clear we are dealing with grepping again. The source code does not give us many vulnerabilities except for the `$key` variable in the grep command which sanitises any linux commands like:
```
/[;|&`\'"]/
```
<img title="inspect html" alt="Alt text" src="../image_resources/natas16_code.png">

The challenge demands a unique approach, especially given the filters and constraints we're working within. I attempted to combine the path from a previous grepping challenge /etc/natas_webpass/natas17 with a strategy from the previous level.

The approach involved iterating through potential passwords chars using the grep command:
```
$(grep -E ^<password + char>.* /etc/natas_webpass/natas17)Africans
```
where:
    - The $(...) syntax spawns a subshell, which allows us to execute nested    commands.
    - The Africans string at the start acts as a filter to check if the returned result is NULL, and if so, add the char to the password string.

An image of a certain iteration without correct password input.
<img title="inspect html" alt="Alt text" src="../image_resources/natas16_filter.png">

Through iterating through all the chars, we can get the password. You can also refer to the source code provided for a demonstration.


### Protecting against command injections
Similarly, to the sql injections, there is also a way to protect ourselves from command injections: 
1. Always sanitise and validate inputs to make sure they are not trying to inject anything into your system. For example:
    - quote the data tp enforce that it's the data to be intepreted
    - Removing meta-characters like %27 which are escape sequences that expand to a single quote
2. Try to containerise your system and only set the least privilege access to users.

You can also refer to the source code for a demonstration on how the attack works.