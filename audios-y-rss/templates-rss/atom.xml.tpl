<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>{{ titulo }}</title>
        <link>{{ link }}</link>
        <description>{{ descripcion }}</description>
        <language>{{ lenguaje }}</language>
        <ttl>{{ ttl_minutos }}</ttl>
        <lastBuildDate>{{ ultima_compilacion }}</lastBuildDate>

        <image>
            <title>{{ imagen_titulo }}</title>
            <url>{{ imagen_url }}</url>
            <link>{{ imagen_link }}</link>
        </image>

        {% if webmaster_email %}
        <webMaster>{{ webmaster_email }}</webMaster>
        {% endif %}

        {% if editor_email %}
        <managingEditor>{{ editor_email }}</managingEditor>
        {% endif %}

        {% for item in items %}
        <item>
            <title>{{ item.titulo }}</title>
            <guid>{{ item.guid }}</guid>
            <link>{{ item_link }}</link>
            <pubDate>{{ item.fecha_publicacion }}</pubDate>
            <description>{{ item.descripcion }}</description>
            {# aqui va la URL al audio, lo importante #}
            <enclosure url="{{ item.url_audio }}" length="{{ item.audio_size_bytes }}" type="audio/mpeg"/>

        </item>
        {% endfor %}

    </channel>
</rss>
