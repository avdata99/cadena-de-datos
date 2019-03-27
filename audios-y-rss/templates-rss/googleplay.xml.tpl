<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:googleplay="http://www.google.com/schemas/play-podcasts/1.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
	<channel>
		<title> {{ titulo }}</title>
		<link>{{ link }}</link>
		<language>{{ lenguaje }}</language>
		<copyright></copyright>
		<googleplay:author>{{ autor }}</googleplay:author>
		<googleplay:email>{{ webmaster_email }}</googleplay:email>
		<googleplay:image href='{{ imagen_url }}'/>
		<googleplay:description>{{ descripcion }}</googleplay:description>
		<googleplay:explicit>No</googleplay:explicit>
		<itunes:author>{{ autor }}</itunes:author>
		<itunes:owner>
            <itunes:name>{{ autor }}</itunes:name>
            <itunes:email>{{ editor_email }}</itunes:email>
        </itunes:owner>

		<!-- <googleplay:category text="CATEGORY NAME HERE"/> -->
        {% for item in episodios %}
        <item>
			<title>{{ item.titulo }}</title>
			<googleplay:description><![CDATA[{{ item.descripcion }}
			{% if item.ideas %}
            <br />Ideas: <ul>{% for idea in item.ideas %}
            <li>{{ idea }}</li>{% endfor %}
            </ul>]]>{% endif %}
			 </googleplay:description>
			<googleplay:author>{{ autor }}</googleplay:author>
			<googleplay:image href='{{ item.url_imagen }}'/>
			<googleplay:explicit>No</googleplay:explicit>
            <enclosure url="{{ item.url_audio }}" length="{{ item.audio_size_bytes }}" type="audio/x-mp3"/>
			<guid>{{ item.guid }}</guid>
			<pubDate>{{ item.fecha_publicacion }}</pubDate>
		</item>
        {% endfor %}
	</channel>
</rss>