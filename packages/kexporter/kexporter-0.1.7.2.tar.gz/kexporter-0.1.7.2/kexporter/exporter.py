import os, discord, re
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape

profile_cache = {}
CACHE_DURATION = timedelta(minutes=5)
env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    autoescape=select_autoescape(["html", "xml"])
)

async def get_member_profile_data(member, bot):
    try:
        accent_color = None
        if isinstance(member, discord.Member) and member.color and member.color.value:
            accent_color = format_color(member.color.value)
        return None, accent_color
    except Exception as e:
        print(f"Erreur: {e}")
        return None, None

def get_member_color(member):
    if not isinstance(member, discord.Member):
        return None
        
    colored_roles = [role for role in member.roles[1:] if role.color.value != 0]
    
    if colored_roles:
        return colored_roles[-1].color.value
    return None

def unicode_to_twemoji(emoji_char):
    if len(emoji_char) == 0:
        return None
    try:
        codes = [f"{ord(char):x}" for char in emoji_char]
        filename = "-".join(codes)
        return f"https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{filename}.svg"
    except Exception:
        return None

def format_color(color_value):
    if isinstance(color_value, int):
        return f"{color_value:06x}"
    elif hasattr(color_value, 'value'):
        return f"{color_value.value:06x}"
    return None

def format_markdown(content, bot):
    if not content:
        return ""
    
    content = re.sub(r'```(\w+)?\n(.*?)\n```', lambda m: f'<div class="code-block"><pre><code class="language-{m.group(1) or ""}">{m.group(2)}</code></pre></div>', content, flags=re.DOTALL)
    
    content = re.sub(r'<@!?(\d+)>', lambda m: f'<span class="mention">@{get_user_name(bot, int(m.group(1)))}</span>', content)
    content = re.sub(r'<#(\d+)>', lambda m: f'<span class="mention">#{get_channel_name(bot, int(m.group(1)))}</span>', content)
    content = re.sub(r'<(a)?:([a-zA-Z0-9_]+):(\d+)>', lambda m: f'<img class="emoji" src="https://cdn.discordapp.com/emojis/{m.group(3)}.{"gif" if m.group(1) else "png"}" alt="{m.group(2)}">', content)
    content = re.sub(r'<:([a-zA-Z0-9_]+):(\d+)>', r'<img class="emoji" src="https://cdn.discordapp.com/emojis/\2.png" alt="\1">', content)
    content = re.sub(r'<a:([a-zA-Z0-9_]+):(\d+)>', r'<img class="emoji" src="https://cdn.discordapp.com/emojis/\2.gif" alt="\1">', content)
    def replace_emoji(match):
        emoji = match.group(0)
        twemoji_url = unicode_to_twemoji(emoji)
        if twemoji_url:
            return f'<img class="emoji twemoji" src="{twemoji_url}" alt="{emoji}">'
        return emoji

    emoji_pattern = r'[\U0001F300-\U0001F9FF\u200d\u2600-\u26FF\u2700-\u27BF\u2934-\u2935\u2B05-\u2B07]+'
    content = re.sub(emoji_pattern, replace_emoji, content)

    content = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', content, flags=re.MULTILINE)
    
    content = re.sub(r'\|\|(.*?)\|\|', r'<span class="spoiler-container spoiler-hidden">\1</span>', content)
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'_(.*?)_', r'<em>\1</em>', content)
    content = re.sub(r'`(.*?)`', r'<code class="inline-code">\1</code>', content)
    
    return content

def format_embed_content(content, bot):
    if not content:
        return ""
    
    content = re.sub(r'^# (.+)$', r'<h1 class="discord-h1">\1</h1>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2 class="discord-h2">\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3 class="discord-h3">\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^-# (.+)$', r'<div class="discord-secondary">\1</div>', content, flags=re.MULTILINE)
    content = re.sub(r'```(\w+)?\n(.*?)\n```', lambda m: f'<div class="code-block"><pre><code class="language-{m.group(1) or ""}">{m.group(2)}</code></pre></div>', content, flags=re.DOTALL)
    content = re.sub(r'^\s*-\s+(.+)$', r'<div class="list-item">• \1</div>', content, flags=re.MULTILINE)
    content = re.sub(r'>>>\s*([\s\S]*?)(?=\n\n|$)', r'<blockquote class="quote-multiple">\1</blockquote>', content)
    content = re.sub(r'^>\s*(.+)$', r'<blockquote>\1</blockquote>', content, flags=re.MULTILINE)
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
    content = re.sub(r'~~(.*?)~~', r'<span class="strikethrough">\1</span>', content)
    content = re.sub(r'__(.*?)__', r'<span class="underline">\1</span>', content)
    content = re.sub(r'<(a)?:([a-zA-Z0-9_]+):(\d+)>', lambda m: f'<img class="emoji" src="https://cdn.discordapp.com/emojis/{m.group(3)}.{"gif" if m.group(1) else "png"}" alt="{m.group(2)}">', content)
    content = re.sub(r'<(a)?:([a-zA-Z0-9_]+):(\d+)>', r'<img class="emoji" src="https://cdn.discordapp.com/emojis/\3.\2" alt="\2">', content)
    content = re.sub(r'<@!?(\d+)>', lambda m: f'<span class="mention">@{get_user_name(bot, int(m.group(1)))}</span>', content)
    
    return content

def get_user_name(bot, user_id):
    user = bot.get_user(user_id)
    return user.display_name if user else "Utilisateur inconnu"

def get_channel_name(bot, channel_id):
    channel = bot.get_channel(channel_id)
    return channel.name if channel else "channel-inconnu"

def format_timestamp(timestamp):
    if not timestamp:
        return ""
    
    if timestamp.tzinfo:
        timestamp = timestamp.astimezone()
    
    now = datetime.now()
    if timestamp.date() == now.date():
        return timestamp.strftime("%H:%M")
    elif timestamp.date() == (now.date() - timedelta(days=1)):
        return "Hier " + timestamp.strftime("%H:%M")
    else:
        return timestamp.strftime("%d/%m/%Y %H:%M")

env.filters["format_timestamp"] = format_timestamp

async def export(channel, bot, output_path="export.html", include_attachments=False, limit=None, filter_pins=False):
    raw_messages = []
    message_count = 0
    unique_authors = set()
    
    async for msg in channel.history(limit=limit):
        if not (filter_pins and not msg.pinned):
            raw_messages.append(msg)
            message_count += 1
            if not msg.author.bot:
                unique_authors.add(msg.author.id)
    
    unique_users = len(unique_authors)
    
    messages = []
    for msg in raw_messages:
        banner_url, accent_color = await get_member_profile_data(msg.author, bot)
        all_roles = []
        highest_role = None
        if isinstance(msg.author, discord.Member):
            all_roles = [{"name": role.name, "color": role.color.value if role.color else None} 
                    for role in msg.author.roles if role.name != "@everyone"]
            highest_role = max(msg.author.roles[1:], key=lambda r: r.position) if len(msg.author.roles) > 1 else None
            member_color = get_member_color(msg.author)
        message_data = {
            "author": {
                "id": str(msg.author.id),
                "name": msg.author.display_name,
                "color": member_color,
                "avatar_url": msg.author.display_avatar.url,
                "banner_url": banner_url,
                "accent_color": accent_color,
                "is_bot": msg.author.bot,
                "highest_role": {"name": highest_role.name, "color": highest_role.color.value if highest_role and highest_role.color else None} if highest_role else None,
                "all_roles": all_roles,
            },
            "timestamp": msg.created_at,
            "content": format_markdown(msg.content, bot),
            "attachments": [],
            "embeds": [],
            "buttons": [],
            "reactions": [],
            "edited_at": msg.edited_at,
            "pinned": msg.pinned,
            "reply_to": None
        }
    
        if msg.reference and isinstance(msg.reference.resolved, discord.Message):
            message_data["reply_to"] = {
                "author": msg.reference.resolved.author.display_name,
                "content": msg.reference.resolved.content[:100] + "..." if len(msg.reference.resolved.content) > 100 else msg.reference.resolved.content
            }
    
        for attachment in msg.attachments:
            message_data["attachments"].append({
                "filename": attachment.filename,
                "url": attachment.url if include_attachments else None,
                "size": attachment.size
            })

        for embed in msg.embeds:
            embed_data = {
                "author": {
                    "name": format_embed_content(embed.author.name, bot) if embed.author else None,
                    "icon_url": embed.author.icon_url if embed.author else None,
                    "url": embed.author.url if embed.author else None
                } if embed.author else None,
                "title": format_embed_content(embed.title, bot) if embed.title else None,
                "url": embed.url if embed.url else None,
                "description": format_embed_content(embed.description, bot) if embed.description else None,
                "color": embed.color.value if embed.color else None,
                "fields": [{
                    "name": format_embed_content(field.name, bot),
                    "value": format_embed_content(field.value, bot),
                    "inline": field.inline
                } for field in embed.fields],
                "footer": {
                    "text": format_embed_content(embed.footer.text, bot) if embed.footer else None,
                    "icon_url": embed.footer.icon_url if embed.footer and embed.footer.icon_url else None
                } if embed.footer else None,
                "thumbnail_url": embed.thumbnail.url if embed.thumbnail else None,
                "image_url": embed.image.url if embed.image else None,
                "timestamp": embed.timestamp if embed.timestamp else None
            }
            message_data["embeds"].append(embed_data)

        message_data["components"] = []
        if isinstance(msg, discord.Message):
            components_data = msg.components() if callable(msg.components) else msg.components
            if components_data:
                message_data["components"] = [
                    {
                        "type": "row",
                        "items": [
                            {
                                "type": component.type.value,
                                "label": component.label if hasattr(component, 'label') else None,
                                "style": component.style.name.lower() if hasattr(component, 'style') else None,
                                "emoji": str(component.emoji) if hasattr(component, 'emoji') and component.emoji else None,
                                "url": component.url if hasattr(component, 'url') else None,
                                "disabled": component.disabled if hasattr(component, 'disabled') else False,
                                "placeholder": component.placeholder if hasattr(component, 'placeholder') else None,
                                "options": [
                                    {
                                        "label": option.label,
                                        "description": option.description,
                                        "emoji": str(option.emoji) if option.emoji else None,
                                        "default": option.default
                                    } for option in component.options
                                ] if hasattr(component, 'options') else None
                            } for component in row.children
                        ]
                    } for row in components_data
                ]

        message_data["reactions"] = []
        if hasattr(msg, 'reactions') and len(msg.reactions) > 0:
            for reaction in msg.reactions:
                if isinstance(reaction, discord.reaction.Reaction):
                    emoji_str = str(reaction.emoji)
                    is_custom = '<:' in emoji_str or '<a:' in emoji_str
                    
                    if is_custom:
                        match = re.match(r'<(a)?:([a-zA-Z0-9_]+):(\d+)>', emoji_str)
                        if match:
                            animated = match.group(1) is not None
                            name = match.group(2)
                            emoji_id = match.group(3)
                            final_emoji = f'<img class="emoji" src="https://cdn.discordapp.com/emojis/{emoji_id}.{"gif" if animated else "png"}" alt="{name}">'
                    else:
                        final_emoji = emoji_str

                    message_data["reactions"].append({
                        "emoji": final_emoji,
                        "count": reaction.count,
                        "is_custom": is_custom
                    })

        messages.append(message_data)

    css_path = os.path.join(os.path.dirname(__file__), "static", "style.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            style_content = f.read()
    except FileNotFoundError:
        style_content = "/* CSS non trouvé */"

    template = env.get_template("base.html")
    rendered = template.render(
        messages=reversed(messages),
        channel_name=channel.name,
        channel_topic=channel.topic if hasattr(channel, 'topic') else None,
        export_date=datetime.now().strftime("%d/%m/%Y %H:%M"),
        include_attachments=include_attachments,
        style_content=style_content,
        message_count=message_count,
        unique_users=unique_users
    )
    if rendered is None:
        rendered = ""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    return rendered