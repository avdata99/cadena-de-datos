<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
    <channel>
        <title>{{ titulo }}</title>
        <link>{{ link }}</link>
        <description>{{ descripcion }}</description>
        <itunes:summary>{{ descripcion }}</itunes:summary>
        <itunes:author>{{ autor }}</itunes:author>
        <language>{{ lenguaje }}</language>
        <ttl>{{ ttl_minutos }}</ttl>
        <lastBuildDate>{{ ultima_compilacion }}</lastBuildDate>

        <image>
            <title>{{ imagen_titulo }}</title>
            <url>{{ imagen_url }}</url>
            <link>{{ imagen_link }}</link>
        </image>
        <itunes:image href="{{ imagen_url }}" />
        <itunes:explicit>No</itunes:explicit>
        {% if webmaster_email %}
        <webMaster>{{ webmaster_email }}</webMaster>
        {% endif %}

        {% if editor_email %}
        <managingEditor>{{ editor_email }}</managingEditor>
        {% endif %}

        {% for item in episodios %}
        <item>
            <title>{{ item.titulo }}</title>
            <guid>{{ item.guid }}</guid>
            <link>{{ item.link }}</link>
            <pubDate>{{ item.fecha_publicacion }}</pubDate>
            <description><![CDATA[{{ item.descripcion }}
            <br />Ideas: {% for idea in ideas %}<ul>
            <li>{{ idea }}</li>{% endfor %}
            </ul>]]>
            </description>
            <itunes:summary>{{ item.descripcion }}</itunes:summary>
            {# aqui va la URL al audio, lo importante #}
            <enclosure url="{{ item.url_audio }}" length="{{ item.audio_size_bytes }}" type="audio/mpeg"/>

            <itunes:image href="{{ item.url_imagen }}" />

        </item>
        {% endfor %}

    </channel>
</rss>