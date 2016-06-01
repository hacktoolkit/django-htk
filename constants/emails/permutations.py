# inspired by Email Permuator by Rob Ousbey
# dis.tl/name2email
# http://www.distilled.net/blog/miscellaneous/find-almost-anybodys-email-address/

# variables are:
# fn - firstname
# fi - first initial
# mn - middle name
# mi - middle initial
# ln - lastname
# li - last initial

EMAIL_PERMUTATION_PATTERNS = (
    # Simple:
    '{fn}',
    '{ln}',
    # Basics:
    '{fn}{ln}',
    '{fn}.{ln}',
    '{fi}{ln}',
    '{fi}.{ln}',
    '{fn}{li}',
    '{fn}.{li}',
    '{fi}{li}',
    '{fi}.{li}',
    # Backwards:
    '{ln}{fn}',
    '{ln}.{fn}',
    '{ln}{fi}',
    '{ln}.{fi}',
    '{li}{fn}',
    '{li}.{fn}',
    '{li}{fi}',
    '{li}.{fi}',
    # Using Middle Name:
    '{fi}{mi}{ln}',
    '{fi}{mi}.{ln}',
    '{fn}{mi}{ln}',
    '{fn}.{mi}.{ln}',
    '{fn}{mn}{ln}',
    '{fn}.{mn}.{ln}',
    # Dashes:
    '{fn}-{ln}',
    '{fi}-{ln}',
    '{fn}-{li}',
    '{fi}-{li}',
    '{ln}-{fn}',
    '{ln}-{fi}',
    '{li}-{fn}',
    '{li}-{fi}',
    '{fi}{mi}-{ln}',
    '{fn}-{mi}-{ln}',
    '{fn}-{mn}-{ln}',
    # Underscores
    '{fn}_{ln}',
    '{fi}_{ln}',
    '{fn}_{li}',
    '{fi}_{li}',
    '{ln}_{fn}',
    '{ln}_{fi}',
    '{li}_{fn}',
    '{li}_{fi}',
    '{fi}{mi}_{ln}',
    '{fn}_{mi}_{ln}',
    '{fn}_{mn}_{ln}',
)
