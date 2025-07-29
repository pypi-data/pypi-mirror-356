:py:mod:`simpledali.abstractdali`
=================================

.. py:module:: simpledali.abstractdali

.. autodoc2-docstring:: simpledali.abstractdali
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`DataLink <simpledali.abstractdali.DataLink>`
     -

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`DLPROTO_1_0 <simpledali.abstractdali.DLPROTO_1_0>`
     - .. autodoc2-docstring:: simpledali.abstractdali.DLPROTO_1_0
          :summary:
   * - :py:obj:`DLPROTO_1_1 <simpledali.abstractdali.DLPROTO_1_1>`
     - .. autodoc2-docstring:: simpledali.abstractdali.DLPROTO_1_1
          :summary:
   * - :py:obj:`NO_SOUP <simpledali.abstractdali.NO_SOUP>`
     - .. autodoc2-docstring:: simpledali.abstractdali.NO_SOUP
          :summary:
   * - :py:obj:`QUERY_MODE <simpledali.abstractdali.QUERY_MODE>`
     - .. autodoc2-docstring:: simpledali.abstractdali.QUERY_MODE
          :summary:
   * - :py:obj:`STREAM_MODE <simpledali.abstractdali.STREAM_MODE>`
     - .. autodoc2-docstring:: simpledali.abstractdali.STREAM_MODE
          :summary:

API
~~~

.. py:data:: DLPROTO_1_0
   :canonical: simpledali.abstractdali.DLPROTO_1_0
   :value: '1.0'

   .. autodoc2-docstring:: simpledali.abstractdali.DLPROTO_1_0

.. py:data:: DLPROTO_1_1
   :canonical: simpledali.abstractdali.DLPROTO_1_1
   :value: '1.1'

   .. autodoc2-docstring:: simpledali.abstractdali.DLPROTO_1_1

.. py:data:: NO_SOUP
   :canonical: simpledali.abstractdali.NO_SOUP
   :value: 'Write permission not granted, no soup for you!'

   .. autodoc2-docstring:: simpledali.abstractdali.NO_SOUP

.. py:data:: QUERY_MODE
   :canonical: simpledali.abstractdali.QUERY_MODE
   :value: 'query'

   .. autodoc2-docstring:: simpledali.abstractdali.QUERY_MODE

.. py:data:: STREAM_MODE
   :canonical: simpledali.abstractdali.STREAM_MODE
   :value: 'stream'

   .. autodoc2-docstring:: simpledali.abstractdali.STREAM_MODE

.. py:class:: DataLink(packet_size=-1, dlproto=DLPROTO_1_0, verbose=False)
   :canonical: simpledali.abstractdali.DataLink

   Bases: :py:obj:`abc.ABC`

   .. py:method:: __aenter__()
      :canonical: simpledali.abstractdali.DataLink.__aenter__
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.__aenter__

   .. py:method:: __aexit__(exc_type, exc, tb)
      :canonical: simpledali.abstractdali.DataLink.__aexit__
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.__aexit__

   .. py:method:: createDaliConnection()
      :canonical: simpledali.abstractdali.DataLink.createDaliConnection
      :abstractmethod:
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.createDaliConnection

   .. py:method:: send(header, data)
      :canonical: simpledali.abstractdali.DataLink.send
      :abstractmethod:
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.send

   .. py:method:: parseResponse()
      :canonical: simpledali.abstractdali.DataLink.parseResponse
      :abstractmethod:
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.parseResponse

   .. py:method:: isClosed()
      :canonical: simpledali.abstractdali.DataLink.isClosed
      :abstractmethod:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.isClosed

   .. py:method:: close()
      :canonical: simpledali.abstractdali.DataLink.close
      :abstractmethod:
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.close

   .. py:method:: _force_close()
      :canonical: simpledali.abstractdali.DataLink._force_close
      :abstractmethod:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink._force_close

   .. py:method:: isQueryMode()
      :canonical: simpledali.abstractdali.DataLink.isQueryMode

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.isQueryMode

   .. py:method:: isStreamMode()
      :canonical: simpledali.abstractdali.DataLink.isStreamMode

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.isStreamMode

   .. py:method:: updateMode(header)
      :canonical: simpledali.abstractdali.DataLink.updateMode

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.updateMode

   .. py:method:: write(streamid, hpdatastart, hpdataend, flags, data, pktid=None)
      :canonical: simpledali.abstractdali.DataLink.write
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.write

   .. py:method:: writeAck(streamid, hpdatastart, hpdataend, data, pktid=None)
      :canonical: simpledali.abstractdali.DataLink.writeAck
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.writeAck

   .. py:method:: writeMSeed(msr, pktid=None)
      :canonical: simpledali.abstractdali.DataLink.writeMSeed
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.writeMSeed

   .. py:method:: writeMSeed3(ms3, pktid=None)
      :canonical: simpledali.abstractdali.DataLink.writeMSeed3
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.writeMSeed3

   .. py:method:: writeJSON(streamid, hpdatastart, hpdataend, jsonMessage, pktid=None)
      :canonical: simpledali.abstractdali.DataLink.writeJSON
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.writeJSON

   .. py:method:: writeBZ2JSON(streamid, hpdatastart, hpdataend, jsonMessage, pktid=None)
      :canonical: simpledali.abstractdali.DataLink.writeBZ2JSON
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.writeBZ2JSON

   .. py:method:: writeCommand(command, dataString=None)
      :canonical: simpledali.abstractdali.DataLink.writeCommand
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.writeCommand

   .. py:method:: auth(token)
      :canonical: simpledali.abstractdali.DataLink.auth
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.auth

   .. py:method:: id(programname, username, processid, architecture)
      :canonical: simpledali.abstractdali.DataLink.id
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.id

   .. py:method:: info(infotype)
      :canonical: simpledali.abstractdali.DataLink.info
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.info

   .. py:method:: positionSet(packetId, packetTime=None)
      :canonical: simpledali.abstractdali.DataLink.positionSet
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.positionSet

   .. py:method:: positionEarliest()
      :canonical: simpledali.abstractdali.DataLink.positionEarliest
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.positionEarliest

   .. py:method:: positionLatest()
      :canonical: simpledali.abstractdali.DataLink.positionLatest
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.positionLatest

   .. py:method:: positionAfter(time)
      :canonical: simpledali.abstractdali.DataLink.positionAfter
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.positionAfter

   .. py:method:: positionAfterHPTime(hpdatastart)
      :canonical: simpledali.abstractdali.DataLink.positionAfterHPTime
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.positionAfterHPTime

   .. py:method:: match(pattern)
      :canonical: simpledali.abstractdali.DataLink.match
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.match

   .. py:method:: reject(pattern)
      :canonical: simpledali.abstractdali.DataLink.reject
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.reject

   .. py:method:: read(packetId)
      :canonical: simpledali.abstractdali.DataLink.read
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.read

   .. py:method:: readEarliest()
      :canonical: simpledali.abstractdali.DataLink.readEarliest
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.readEarliest

   .. py:method:: readLatest()
      :canonical: simpledali.abstractdali.DataLink.readLatest
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.readLatest

   .. py:method:: stream()
      :canonical: simpledali.abstractdali.DataLink.stream
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.stream

   .. py:method:: startStream()
      :canonical: simpledali.abstractdali.DataLink.startStream
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.startStream

   .. py:method:: endStream()
      :canonical: simpledali.abstractdali.DataLink.endStream
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.endStream

   .. py:method:: reconnect()
      :canonical: simpledali.abstractdali.DataLink.reconnect
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.reconnect

   .. py:method:: parsedInfoStatus()
      :canonical: simpledali.abstractdali.DataLink.parsedInfoStatus
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.parsedInfoStatus

   .. py:method:: parse_capabilities(cap)
      :canonical: simpledali.abstractdali.DataLink.parse_capabilities

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.parse_capabilities

   .. py:method:: status_xml_to_dict(statusEl)
      :canonical: simpledali.abstractdali.DataLink.status_xml_to_dict

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.status_xml_to_dict

   .. py:method:: parsedInfoStreams()
      :canonical: simpledali.abstractdali.DataLink.parsedInfoStreams
      :async:

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.parsedInfoStreams

   .. py:method:: info_typed(k, v)
      :canonical: simpledali.abstractdali.DataLink.info_typed

      .. autodoc2-docstring:: simpledali.abstractdali.DataLink.info_typed
