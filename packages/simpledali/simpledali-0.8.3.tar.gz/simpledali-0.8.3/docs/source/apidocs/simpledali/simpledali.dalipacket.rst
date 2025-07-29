:py:mod:`simpledali.dalipacket`
===============================

.. py:module:: simpledali.dalipacket

.. autodoc2-docstring:: simpledali.dalipacket
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`DaliResponse <simpledali.dalipacket.DaliResponse>`
     - .. autodoc2-docstring:: simpledali.dalipacket.DaliResponse
          :summary:
   * - :py:obj:`DaliPacket <simpledali.dalipacket.DaliPacket>`
     - .. autodoc2-docstring:: simpledali.dalipacket.DaliPacket
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`nslcToStreamId <simpledali.dalipacket.nslcToStreamId>`
     - .. autodoc2-docstring:: simpledali.dalipacket.nslcToStreamId
          :summary:
   * - :py:obj:`fdsnSourceIdToStreamId <simpledali.dalipacket.fdsnSourceIdToStreamId>`
     - .. autodoc2-docstring:: simpledali.dalipacket.fdsnSourceIdToStreamId
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`JSON_TYPE <simpledali.dalipacket.JSON_TYPE>`
     - .. autodoc2-docstring:: simpledali.dalipacket.JSON_TYPE
          :summary:
   * - :py:obj:`BZ2_JSON_TYPE <simpledali.dalipacket.BZ2_JSON_TYPE>`
     - .. autodoc2-docstring:: simpledali.dalipacket.BZ2_JSON_TYPE
          :summary:
   * - :py:obj:`MSEED_TYPE <simpledali.dalipacket.MSEED_TYPE>`
     - .. autodoc2-docstring:: simpledali.dalipacket.MSEED_TYPE
          :summary:
   * - :py:obj:`MSEED3_TYPE <simpledali.dalipacket.MSEED3_TYPE>`
     - .. autodoc2-docstring:: simpledali.dalipacket.MSEED3_TYPE
          :summary:

API
~~~

.. py:data:: JSON_TYPE
   :canonical: simpledali.dalipacket.JSON_TYPE
   :value: 'JSON'

   .. autodoc2-docstring:: simpledali.dalipacket.JSON_TYPE

.. py:data:: BZ2_JSON_TYPE
   :canonical: simpledali.dalipacket.BZ2_JSON_TYPE
   :value: 'BZJSON'

   .. autodoc2-docstring:: simpledali.dalipacket.BZ2_JSON_TYPE

.. py:data:: MSEED_TYPE
   :canonical: simpledali.dalipacket.MSEED_TYPE
   :value: 'MSEED'

   .. autodoc2-docstring:: simpledali.dalipacket.MSEED_TYPE

.. py:data:: MSEED3_TYPE
   :canonical: simpledali.dalipacket.MSEED3_TYPE
   :value: 'MSEED3'

   .. autodoc2-docstring:: simpledali.dalipacket.MSEED3_TYPE

.. py:class:: DaliResponse(packettype, value, message)
   :canonical: simpledali.dalipacket.DaliResponse

   .. autodoc2-docstring:: simpledali.dalipacket.DaliResponse

   .. rubric:: Initialization

   .. autodoc2-docstring:: simpledali.dalipacket.DaliResponse.__init__

   .. py:method:: __str__()
      :canonical: simpledali.dalipacket.DaliResponse.__str__

.. py:class:: DaliPacket(packettype, streamId, packetId, packetTime, dataStartTime, dataEndTime, dSize, data)
   :canonical: simpledali.dalipacket.DaliPacket

   .. autodoc2-docstring:: simpledali.dalipacket.DaliPacket

   .. rubric:: Initialization

   .. autodoc2-docstring:: simpledali.dalipacket.DaliPacket.__init__

   .. py:method:: streamIdChannel()
      :canonical: simpledali.dalipacket.DaliPacket.streamIdChannel

      .. autodoc2-docstring:: simpledali.dalipacket.DaliPacket.streamIdChannel

   .. py:method:: streamIdType()
      :canonical: simpledali.dalipacket.DaliPacket.streamIdType

      .. autodoc2-docstring:: simpledali.dalipacket.DaliPacket.streamIdType

   .. py:method:: __str__()
      :canonical: simpledali.dalipacket.DaliPacket.__str__

.. py:exception:: DaliException(message, daliResponse=None)
   :canonical: simpledali.dalipacket.DaliException

   Bases: :py:obj:`Exception`

   .. py:method:: __str__()
      :canonical: simpledali.dalipacket.DaliException.__str__

.. py:exception:: DaliClosed(message)
   :canonical: simpledali.dalipacket.DaliClosed

   Bases: :py:obj:`simpledali.dalipacket.DaliException`

.. py:function:: nslcToStreamId(net: str, sta: str, loc: str, chan: str, packettype: str) -> str
   :canonical: simpledali.dalipacket.nslcToStreamId

   .. autodoc2-docstring:: simpledali.dalipacket.nslcToStreamId

.. py:function:: fdsnSourceIdToStreamId(sourceId: simplemseed.FDSNSourceId, packettype: str, trimFDSN=False) -> str
   :canonical: simpledali.dalipacket.fdsnSourceIdToStreamId

   .. autodoc2-docstring:: simpledali.dalipacket.fdsnSourceIdToStreamId
