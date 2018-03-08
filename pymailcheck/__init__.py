#!env/bin/python
"""Port of mailcheck.js

https://github.com/dbarlett/pymailcheck/
"""

DOMAIN_THRESHOLD = 2
SECOND_LEVEL_THRESHOLD = 2
TOP_LEVEL_THRESHOLD = 2
DOMAINS = frozenset([
    "aim.com",
    "aol.com",
    "att.net",
    "bellsouth.net",
    "btinternet.com",
    "charter.net",
    "comcast.net",
    "cox.net",
    "earthlink.net",
    "gmail.com",
    "google.com",
    "googlemail.com",
    "icloud.com",
    "mac.com",
    "me.com",
    "msn.com",
    "optonline.net",
    "optusnet.com.au",
    "qq.com",
    "rocketmail.com",
    "rogers.com",
    "sbcglobal.net",
    "shaw.ca",
    "sky.com",
    "sympatico.ca",
    "telus.net",
    "verizon.net",
    "web.de",
    "xtra.co.nz",
    "ymail.com",
])
SECOND_LEVEL_DOMAINS = frozenset([
    "gmx"
    "hotmail",
    "live",
    "mail",
    "outlook",
    "yahoo",
])
TOP_LEVEL_DOMAINS = frozenset([
    "at",
    "be",
    "biz",
    "ca",
    "ch",
    "co.il",
    "co.jp",
    "co.nz",
    "co.uk",
    "com",
    "com.au",
    "com.tw",
    "cz",
    "de",
    "dk",
    "edu",
    "es",
    "eu",
    "fr",
    "gov",
    "gr",
    "hk",
    "hu"
    "ie",
    "in",
    "info",
    "it",
    "jp",
    "kr",
    "mil",
    "net",
    "net",
    "net.au",
    "nl",
    "no",
    "org",
    "ru",
    "se",
    "sg",
    "us",
])


def sift3_distance(s_1, s_2, max_offset=5):
    """Calculate string distance

    See http://siderite.blogspot.com/2007/04/super-fast-and-accurate-string-\
distance.html for background. This is a port of sift3Distance from mailcheck.js
    rather than the Python code from https://gist.github.com/fjorgemota/3067867
    because the latter produces different results.

    :param s_1: first string
    :param s_2: second string
    :param max_offset: maximum offset, default: 5
    :type s_1: str
    :type s_2: str
    :type max_offset: int
    :returns: string distance
    :rtype: int
    """
    len_s_1 = len(s_1)
    len_s_2 = len(s_2)

    if len_s_1 == 0:
        if len_s_2 == 0:
            return 0
        else:
            return len_s_2

    if len_s_2 == 0:
        return len_s_1

    c = 0
    offset_1 = 0
    offset_2 = 0
    lcs = 0

    while (c + offset_1 < len_s_1) and (c + offset_2 < len_s_2):
        if s_1[c + offset_1] == s_2[c + offset_2]:
            lcs += 1
        else:
            offset_1 = 0
            offset_2 = 0
            for i in range(0, max_offset):
                if (c + i < len_s_1) and (s_1[c + i] == s_2[c]):
                    offset_1 = i
                    break
                if (c + i < len_s_2) and (s_1[c] == s_2[c + i]):
                    offset_2 = i
                    break
        c += 1
    return (len_s_1 + len_s_2) / 2.0 - lcs


def split_email(email):
    """Split an email address

    :param email: email address
    :type email: str
    :returns: email address parts, or False if not an email address
    :rtype: dict, bool
    """
    parts = email.strip().split("@")
    if len(parts) < 2:
        return False
    for i in parts:
        if i == "":
            return False

    domain = parts.pop()
    domain_parts = domain.split(".")
    sld = ""
    tld = ""

    if len(domain_parts) == 0:
        # The address does not have a top-level domain
        return False
    elif len(domain_parts) == 1:
        # The address has only a top-level domain (valid under RFC)
        tld = domain_parts[0]
    else:
        sld = domain_parts[0]
        for i in domain_parts[1:]:
            tld += (i + ".")
        tld = tld[0:-1]

    return {
        "address": "@".join(parts),
        "top_level_domain": tld,
        "second_level_domain": sld,
        "domain": domain,
    }


def find_closest_domain(
        domain,
        domains,
        threshold=DOMAIN_THRESHOLD
):
    """Find closest domain

    :param domain: domain
    :param domains: domains to compare to
    :param threshold: distance threshold
    :returns: closest domain, or False if none is less than or equal to
    threshold
    :rtype: str, bool
    """
    min_dist = 99
    closest_domain = None

    for i in domains:
        if domain == i:
            return domain
        dist = sift3_distance(domain, i)
        if dist < min_dist:
            min_dist = dist
            closest_domain = i

    if min_dist <= threshold and closest_domain is not None:
        return closest_domain
    else:
        return False


def suggest(
        email,
        domains=DOMAINS,
        second_level_domains=SECOND_LEVEL_DOMAINS,
        top_level_domains=TOP_LEVEL_DOMAINS
):
    """Suggest a corrected email address

    :param email: email address
    :param domains: domains to match against, default DOMAINS
    :param second_level_domains: second-level domains to match against,
     default SECOND_LEVEL DOMAINS
    :param top_level_domains: top-level domains to matcha against,
     default TOP_LEVEL_DOMAINS
    :type email: str
    :type domains: list
    :type second_level_domains: iterable
    :type top_level_domains: iterable
    :returns: email suggestion, or False
    :rtype: dict, bool
    """
    email = email.lower()
    email_parts = split_email(email)

    # If the email is invalid, or a valid 2nd-level + top-level, do not suggest
    # anything.
    if not email_parts or (
            email_parts["second_level_domain"] in second_level_domains and
            email_parts["top_level_domain"] in top_level_domains
    ):
        return False

    closest_domain = find_closest_domain(
        email_parts["domain"],
        domains
    )
    if closest_domain:
        if closest_domain == email_parts["domain"]:
            # The email address exactly matches one of the supplied domains; do
            # not return a suggestion.
            return False
        else:
            # The email address closely matches one of the supplied domains;
            # return a suggestion
            return {
                "address": email_parts["address"],
                "domain": closest_domain,
                "full": "{0}@{1}".format(
                    email_parts["address"],
                    closest_domain
                )
            }

    closest_sld = find_closest_domain(
        email_parts["second_level_domain"],
        second_level_domains
    )
    closest_tld = find_closest_domain(
        email_parts["top_level_domain"],
        top_level_domains
    )
    if email_parts["domain"]:
        closest_domain = email_parts["domain"]
        ret = False

        if closest_sld and closest_sld != email_parts["second_level_domain"]:
            # The email address may have a misspelled second-level domain;
            # return a suggestion.
            closest_domain = closest_domain.replace(
                email_parts["second_level_domain"],
                closest_sld
            )
            ret = True

        if closest_tld and closest_tld != email_parts["top_level_domain"]:
            # The email address may have a misspelled top-level domain;
            # return a suggestion.
            closest_domain = closest_domain.replace(
                email_parts["top_level_domain"],
                closest_tld
            )
            ret = True

        if ret:
            return {
                "address": email_parts["address"],
                "domain": closest_domain,
                "full": "{0}@{1}".format(
                    email_parts["address"],
                    closest_domain
                )
            }
    # The email address exactly matches one of the supplied domains, does not
    # closely match any domain and does not appear to simply have a mispelled
    # top-level domain, or is an invalid email address; do not return a
    # suggestion.
    return False
