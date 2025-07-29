import { browse } from "./browse.js";
import { Track, VirtualTrack } from "../api.js";

/**
 * Get display HTML for a track
 * @param {Track|VirtualTrack} track
 * @param {boolean} showPlaylist
 * @returns {HTMLSpanElement}
 */
export function trackDisplayHtml(track, showPlaylist = false) {
    const html = document.createElement('span');
    html.classList.add('track-display-html');

    if (track instanceof VirtualTrack) {
        html.textContent = track.title;
        return html;
    }

    if (track.artists.length > 0 && track.title) {
        let first = true;
        for (const artist of track.artists) {
            if (first) {
                first = false;
            } else {
                html.append(', ');
            }

            const artistHtml = document.createElement('a');
            artistHtml.textContent = artist;
            artistHtml.addEventListener("click", () => browse.browseArtist(artist));
            html.append(artistHtml);
        }

        const titleHtml = document.createElement('a');
        titleHtml.textContent = track.title;
        titleHtml.style.color = 'var(--text-color)';
        titleHtml.addEventListener("click", () => browse.browseTitle(track.title));
        html.append(' - ', titleHtml);
    } else {
        const span = document.createElement('span');
        span.style.color = "var(--text-color-warning)";
        span.textContent = track.path.substring(track.path.indexOf('/') + 1);
        html.append(span);
    }

    const secondary = document.createElement('span');
    secondary.classList.add('secondary');
    secondary.append(document.createElement('br'));
    html.append(secondary);

    if (showPlaylist) {
        const playlistHtml = document.createElement('a');
        playlistHtml.addEventListener("click", () => browse.browsePlaylist(track.playlistName));
        playlistHtml.textContent = track.playlistName;
        secondary.append(playlistHtml);
    }

    const year = track.year;
    const album = track.album;
    const albumArtist = track.albumArtist;

    if (year || track.album) {
        if (showPlaylist) {
            secondary.append(', ');
        }

        if (album) {
            const albumHtml = document.createElement('a');
            albumHtml.addEventListener("click", () => browse.browseAlbum(album, albumArtist));
            if (albumArtist) {
                albumHtml.textContent = albumArtist + ' - ' + album;
            } else {
                albumHtml.textContent = album;
            }
            secondary.append(albumHtml);
            if (track.year) {
                secondary.append(', ');
            }
        }

        if (year) {
            const yearHtml = document.createElement('a');
            yearHtml.textContent = year + '';
            yearHtml.addEventListener('click', () => browse.browseYear(year));
            secondary.append(yearHtml);
        }
    }

    return html;
};
