:py:mod:`simpledali.dali2jsonl`
===============================

.. py:module:: simpledali.dali2jsonl

.. autodoc2-docstring:: simpledali.dali2jsonl
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`Dali2Jsonl <simpledali.dali2jsonl.Dali2Jsonl>`
     - .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`do_parseargs <simpledali.dali2jsonl.do_parseargs>`
     - .. autodoc2-docstring:: simpledali.dali2jsonl.do_parseargs
          :summary:
   * - :py:obj:`main <simpledali.dali2jsonl.main>`
     - .. autodoc2-docstring:: simpledali.dali2jsonl.main
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`DEFAULT_HOST <simpledali.dali2jsonl.DEFAULT_HOST>`
     - .. autodoc2-docstring:: simpledali.dali2jsonl.DEFAULT_HOST
          :summary:
   * - :py:obj:`DEFAULT_PORT <simpledali.dali2jsonl.DEFAULT_PORT>`
     - .. autodoc2-docstring:: simpledali.dali2jsonl.DEFAULT_PORT
          :summary:
   * - :py:obj:`Allowed_Flags <simpledali.dali2jsonl.Allowed_Flags>`
     - .. autodoc2-docstring:: simpledali.dali2jsonl.Allowed_Flags
          :summary:

API
~~~

.. py:data:: DEFAULT_HOST
   :canonical: simpledali.dali2jsonl.DEFAULT_HOST
   :value: 'localhost'

   .. autodoc2-docstring:: simpledali.dali2jsonl.DEFAULT_HOST

.. py:data:: DEFAULT_PORT
   :canonical: simpledali.dali2jsonl.DEFAULT_PORT
   :value: 16000

   .. autodoc2-docstring:: simpledali.dali2jsonl.DEFAULT_PORT

.. py:data:: Allowed_Flags
   :canonical: simpledali.dali2jsonl.Allowed_Flags
   :value: ['n', 's', 'l', 'c', 'Y', 'j', 'H']

   .. autodoc2-docstring:: simpledali.dali2jsonl.Allowed_Flags

.. py:class:: Dali2Jsonl(match, writePattern, host=DEFAULT_HOST, port=DEFAULT_PORT, websocketurl=None, verbose=False)
   :canonical: simpledali.dali2jsonl.Dali2Jsonl

   .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl

   .. rubric:: Initialization

   .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl.__init__

   .. py:method:: from_config(conf, verbose=False)
      :canonical: simpledali.dali2jsonl.Dali2Jsonl.from_config
      :classmethod:

      .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl.from_config

   .. py:method:: run()
      :canonical: simpledali.dali2jsonl.Dali2Jsonl.run
      :async:

      .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl.run

   .. py:method:: do_dali(dali)
      :canonical: simpledali.dali2jsonl.Dali2Jsonl.do_dali
      :async:

      .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl.do_dali

   .. py:method:: stream_data(dali)
      :canonical: simpledali.dali2jsonl.Dali2Jsonl.stream_data
      :async:

      .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl.stream_data

   .. py:method:: saveToJSONL(daliPacket)
      :canonical: simpledali.dali2jsonl.Dali2Jsonl.saveToJSONL

      .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl.saveToJSONL

   .. py:method:: fileFromSidPattern(sid: simplemseed.FDSNSourceId, time)
      :canonical: simpledali.dali2jsonl.Dali2Jsonl.fileFromSidPattern

      .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl.fileFromSidPattern

   .. py:method:: fillBaseSidPattern(sid: simplemseed.FDSNSourceId)
      :canonical: simpledali.dali2jsonl.Dali2Jsonl.fillBaseSidPattern

      .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl.fillBaseSidPattern

   .. py:method:: fillTimePattern(base, time)
      :canonical: simpledali.dali2jsonl.Dali2Jsonl.fillTimePattern

      .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl.fillTimePattern

   .. py:method:: checkPattern(p)
      :canonical: simpledali.dali2jsonl.Dali2Jsonl.checkPattern

      .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl.checkPattern

   .. py:method:: configure_defaults(conf)
      :canonical: simpledali.dali2jsonl.Dali2Jsonl.configure_defaults
      :staticmethod:

      .. autodoc2-docstring:: simpledali.dali2jsonl.Dali2Jsonl.configure_defaults

.. py:function:: do_parseargs()
   :canonical: simpledali.dali2jsonl.do_parseargs

   .. autodoc2-docstring:: simpledali.dali2jsonl.do_parseargs

.. py:function:: main()
   :canonical: simpledali.dali2jsonl.main

   .. autodoc2-docstring:: simpledali.dali2jsonl.main
