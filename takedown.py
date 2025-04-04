def generate_takedown_notice(title, url):
    return f"""
    To Whom It May Concern,

    We have detected unauthorized distribution of copyrighted Disney content.

    Title: {title}
    URL: {url}

    Please remove this content immediately under the DMCA.

    Sincerely,  
    Disney Legal Team
    """
