from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.file_list_response import FileListResponse
from ...models.file_response import FileResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    id: Union[None, Unset, int] = UNSET,
    dtyp: Union[None, Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_id: Union[None, Unset, int]
    if isinstance(id, Unset):
        json_id = UNSET
    else:
        json_id = id
    params["id"] = json_id

    json_dtyp: Union[None, Unset, int]
    if isinstance(dtyp, Unset):
        json_dtyp = UNSET
    else:
        json_dtyp = dtyp
    params["dtyp"] = json_dtyp

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/files/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Union["FileListResponse", "FileResponse"]]]:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union["FileListResponse", "FileResponse"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = FileListResponse.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = FileResponse.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, Union["FileListResponse", "FileResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    id: Union[None, Unset, int] = UNSET,
    dtyp: Union[None, Unset, int] = UNSET,
) -> Response[Union[HTTPValidationError, Union["FileListResponse", "FileResponse"]]]:
    """Files

     Abrufen der Dateien (Files) von der Stadt Bonn OParl API.

    Dateien sind Dokumente, die zur Verwaltungsarbeit gehören. Sie können
    Drucksachen, Sitzungsprotokollen, Anlagen oder anderen Dokumenten
    zugeordnet sein.

    Parameter
    ---------
    * **file_id**: ID der spezifischen Datei (optional)
      - Bei Angabe: Einzelne Datei mit allen Details zurück
      - Ohne Angabe: Paginierte Liste aller Dateien zurück
    * **dtyp**: Dokumenttyp

    Rückgabe
    --------
    * **FileResponse**: Einzelne Datei mit Referenzlinks zu lokalen API-URLs
    * **FileListResponse**: Paginierte Liste von Dateien

    Features
    --------
    * Automatische ChromaDB-Indizierung für abgerufene Dateien
    * URL-Umschreibung von Upstream zu lokalen API-Referenzen
    * Hintergrundverarbeitung für Performance
    * Umfassende Fehlerbehandlung
    * Logfire-Observability-Integration

    Hinweise
    --------
    Ein Objekt vom Typ oparl:File kann verschiedene Dokumenttypen repräsentieren,
    einschließlich PDFs, Word-Dokumente, Bilder und andere Dateiformate.

    Siehe: https://oparl.org/spezifikation/online-ansicht/#entity-file

    Args:
        id (Union[None, Unset, int]):
        dtyp (Union[None, Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['FileListResponse', 'FileResponse']]]
    """

    kwargs = _get_kwargs(
        id=id,
        dtyp=dtyp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    id: Union[None, Unset, int] = UNSET,
    dtyp: Union[None, Unset, int] = UNSET,
) -> Optional[Union[HTTPValidationError, Union["FileListResponse", "FileResponse"]]]:
    """Files

     Abrufen der Dateien (Files) von der Stadt Bonn OParl API.

    Dateien sind Dokumente, die zur Verwaltungsarbeit gehören. Sie können
    Drucksachen, Sitzungsprotokollen, Anlagen oder anderen Dokumenten
    zugeordnet sein.

    Parameter
    ---------
    * **file_id**: ID der spezifischen Datei (optional)
      - Bei Angabe: Einzelne Datei mit allen Details zurück
      - Ohne Angabe: Paginierte Liste aller Dateien zurück
    * **dtyp**: Dokumenttyp

    Rückgabe
    --------
    * **FileResponse**: Einzelne Datei mit Referenzlinks zu lokalen API-URLs
    * **FileListResponse**: Paginierte Liste von Dateien

    Features
    --------
    * Automatische ChromaDB-Indizierung für abgerufene Dateien
    * URL-Umschreibung von Upstream zu lokalen API-Referenzen
    * Hintergrundverarbeitung für Performance
    * Umfassende Fehlerbehandlung
    * Logfire-Observability-Integration

    Hinweise
    --------
    Ein Objekt vom Typ oparl:File kann verschiedene Dokumenttypen repräsentieren,
    einschließlich PDFs, Word-Dokumente, Bilder und andere Dateiformate.

    Siehe: https://oparl.org/spezifikation/online-ansicht/#entity-file

    Args:
        id (Union[None, Unset, int]):
        dtyp (Union[None, Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['FileListResponse', 'FileResponse']]
    """

    return sync_detailed(
        client=client,
        id=id,
        dtyp=dtyp,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    id: Union[None, Unset, int] = UNSET,
    dtyp: Union[None, Unset, int] = UNSET,
) -> Response[Union[HTTPValidationError, Union["FileListResponse", "FileResponse"]]]:
    """Files

     Abrufen der Dateien (Files) von der Stadt Bonn OParl API.

    Dateien sind Dokumente, die zur Verwaltungsarbeit gehören. Sie können
    Drucksachen, Sitzungsprotokollen, Anlagen oder anderen Dokumenten
    zugeordnet sein.

    Parameter
    ---------
    * **file_id**: ID der spezifischen Datei (optional)
      - Bei Angabe: Einzelne Datei mit allen Details zurück
      - Ohne Angabe: Paginierte Liste aller Dateien zurück
    * **dtyp**: Dokumenttyp

    Rückgabe
    --------
    * **FileResponse**: Einzelne Datei mit Referenzlinks zu lokalen API-URLs
    * **FileListResponse**: Paginierte Liste von Dateien

    Features
    --------
    * Automatische ChromaDB-Indizierung für abgerufene Dateien
    * URL-Umschreibung von Upstream zu lokalen API-Referenzen
    * Hintergrundverarbeitung für Performance
    * Umfassende Fehlerbehandlung
    * Logfire-Observability-Integration

    Hinweise
    --------
    Ein Objekt vom Typ oparl:File kann verschiedene Dokumenttypen repräsentieren,
    einschließlich PDFs, Word-Dokumente, Bilder und andere Dateiformate.

    Siehe: https://oparl.org/spezifikation/online-ansicht/#entity-file

    Args:
        id (Union[None, Unset, int]):
        dtyp (Union[None, Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['FileListResponse', 'FileResponse']]]
    """

    kwargs = _get_kwargs(
        id=id,
        dtyp=dtyp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    id: Union[None, Unset, int] = UNSET,
    dtyp: Union[None, Unset, int] = UNSET,
) -> Optional[Union[HTTPValidationError, Union["FileListResponse", "FileResponse"]]]:
    """Files

     Abrufen der Dateien (Files) von der Stadt Bonn OParl API.

    Dateien sind Dokumente, die zur Verwaltungsarbeit gehören. Sie können
    Drucksachen, Sitzungsprotokollen, Anlagen oder anderen Dokumenten
    zugeordnet sein.

    Parameter
    ---------
    * **file_id**: ID der spezifischen Datei (optional)
      - Bei Angabe: Einzelne Datei mit allen Details zurück
      - Ohne Angabe: Paginierte Liste aller Dateien zurück
    * **dtyp**: Dokumenttyp

    Rückgabe
    --------
    * **FileResponse**: Einzelne Datei mit Referenzlinks zu lokalen API-URLs
    * **FileListResponse**: Paginierte Liste von Dateien

    Features
    --------
    * Automatische ChromaDB-Indizierung für abgerufene Dateien
    * URL-Umschreibung von Upstream zu lokalen API-Referenzen
    * Hintergrundverarbeitung für Performance
    * Umfassende Fehlerbehandlung
    * Logfire-Observability-Integration

    Hinweise
    --------
    Ein Objekt vom Typ oparl:File kann verschiedene Dokumenttypen repräsentieren,
    einschließlich PDFs, Word-Dokumente, Bilder und andere Dateiformate.

    Siehe: https://oparl.org/spezifikation/online-ansicht/#entity-file

    Args:
        id (Union[None, Unset, int]):
        dtyp (Union[None, Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['FileListResponse', 'FileResponse']]
    """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            dtyp=dtyp,
        )
    ).parsed
